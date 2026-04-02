import logging

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# Configure logging to replace standard print statements for better tracking
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class IterativeRefiner:
    """
    A class that handles iterative retrieval and generation of text.
    It identifies knowledge gaps, generates queries to fill them,
    and iteratively refines the response until it reaches completeness.
    """

    MISSING_MARKER = "[MISSING:"

    def __init__(
        self,
        model_name: str = "openai:gpt-4o-mini",
        temperature: float = 0.7,
    ):
        """
        Initializes the IterativeRefiner with the specified LLM and prompt chains.

        Args:
            model_name (str): The identifier for the LLM model to use.
            temperature (float): The creativity/randomness parameter for the LLM.
        """
        # Load environment variables (e.g., API keys)
        load_dotenv()

        # Initialize the language model
        self.llm = init_chat_model(model_name, temperature=temperature)
        self._initialize_chains()

    def _initialize_chains(self) -> None:
        """
        Initializes the PromptTemplates and LangChain Runnable Chains (LCEL).
        Using `.from_template()` automatically infers variables, which is more Pythonic.
        """
        draft_prompt = PromptTemplate.from_template(
            "You are an expert assistant with limited initial knowledge.\n"
            "Answer the following question, but you MUST mark MANY specific "
            "details as missing.\n"
            "Use [MISSING: ...] markers for:\n"
            "- Specific version numbers and release dates\n"
            "- Technical specifications and parameters\n"
            "- Performance metrics and benchmarks\n"
            "- Comparison data between different versions\n"
            "- Implementation details and code examples\n"
            "- Real-world use cases and case studies\n"
            "- Limitations and known issues\n"
            "- Future roadmap and upcoming features\n\n"
            "Be thorough in identifying what specific information would "
            "make the answer complete.\n"
            "Start with a basic overview but mark MANY specific details as missing.\n\n"
            "Do not generate more than 5 MISSING Markers.\n"
            "Question: {question}\n\n"
            "Answer:"
        )

        query_prompt = PromptTemplate.from_template(
            "You received the following draft with gaps:\n{draft}\n\n"
            "For each [MISSING: ...] marker, provide information to fill that gap.\n"
            "Format each as: 'For [MISSING: topic]: provide the actual information'\n"
            "Be specific and provide real data when possible.\n"
            "Example: 'For [MISSING: version numbers]: LangChain is at version 0.1.0, "
            "LangGraph at 0.2.0'\n"
            "List information for each gap, maximum 5 items."
        )

        fill_prompt = PromptTemplate.from_template(
            "Original question: {question}\n\n"
            "Current draft (iteration {iteration}):\n{draft}\n\n"
            "Information to help fill the gaps:\n{queries}\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. You MUST replace AT LEAST 1-2 [MISSING: ...] markers with "
            "concrete information\n"
            "2. ACTUALLY REPLACE the text '[MISSING: xyz]' with real content - "
            "don't keep the marker\n"
            "3. Use the information above to guide what content to add\n"
            "4. Do NOT add any new [MISSING:] markers - only fill "
            "or keep existing ones\n"
            "5. If you cannot fill a gap with certainty, keep it as [MISSING: ...]\n\n"
            "Example of what to do:\n"
            "- WRONG: '[MISSING: version numbers and release dates]' "
            "(keeping the marker)\n"
            "- RIGHT: 'LangChain version 0.1.0 was released in January 2024' "
            "(replacing with content)\n\n"
            "Important: This is iteration {iteration}. You MUST make progress "
            "by filling gaps.\n\n"
            "Rewrite the ENTIRE answer with the [MISSING:] markers replaced:"
        )

        expansion_prompt = PromptTemplate.from_template(
            "Review this draft answer:\n{draft}\n\n"
            "Identify areas that could benefit from MORE specific information.\n"
            "Add new [MISSING: ...] markers for:\n"
            "- Technical details that were glossed over\n"
            "- Specific examples that would clarify concepts\n"
            "- Comparative data that would add context\n"
            "- Implementation specifics that developers would need\n\n"
            "Return the same text but with ADDITIONAL [MISSING: ...] markers "
            "for deeper details:"
        )

        # Build chains using LangChain Expression Language (LCEL)
        self.draft_chain = draft_prompt | self.llm | StrOutputParser()
        self.query_chain = query_prompt | self.llm | StrOutputParser()
        self.fill_chain = fill_prompt | self.llm | StrOutputParser()
        self.expansion_chain = expansion_prompt | self.llm | StrOutputParser()

    def refine(self, question: str, max_iters: int = 10) -> str:
        """
        Performs iterative retrieval and generation with multiple natural rounds.
        Continues until all gaps are filled or the maximum number of iterations
        is reached.

        Args:
            question (str): The initial user question to answer.
            max_iters (int): Maximum number of allowed iterations to refine the answer.

        Returns:
            str: The final refined and completed answer.
        """
        logging.info("Starting initial draft generation...")
        draft = self.draft_chain.invoke({"question": question})

        current_gaps = draft.count(self.MISSING_MARKER)
        logging.info("Initial draft generated. Gaps identified: %s", current_gaps)

        actual_iterations = 0
        consecutive_no_progress = 0

        for iteration in range(1, max_iters + 1):
            actual_iterations = iteration
            current_gaps = draft.count(self.MISSING_MARKER)

            # Check if completion criteria are met
            if current_gaps == 0:
                logging.info("All gaps filled!")

                # Expand to find more gaps only in the early stages
                if iteration <= 2:
                    logging.info("Checking for new areas to expand...")
                    draft = self.expansion_chain.invoke({"draft": draft})
                    current_gaps = draft.count(self.MISSING_MARKER)

                    if current_gaps == 0:
                        logging.info("Answer is comprehensive and complete!")
                        break

                    logging.info("Identified %s new areas for expansion.", current_gaps)
                    consecutive_no_progress = 0
                else:
                    logging.info("Answer is complete after multiple refinements.")
                    break

            logging.info(
                "--- ITERATION %s | Current Gaps: %s ---",
                iteration,
                current_gaps,
            )

            # Generate queries to answer the missing gaps
            queries = self.query_chain.invoke({"draft": draft})

            # Use the newly generated queries to fill the draft's gaps
            draft = self.fill_chain.invoke(
                {
                    "question": question,
                    "draft": draft,
                    "queries": queries,
                    "iteration": iteration,
                }
            )

            # Calculate progress
            new_gaps = draft.count(self.MISSING_MARKER)
            filled = current_gaps - new_gaps
            logging.info(
                "Progress: Filled %s gap(s). %s remaining.",
                filled,
                new_gaps,
            )

            # Stop if the model gets stuck
            if filled <= 0:
                consecutive_no_progress += 1
                if consecutive_no_progress >= 3:
                    logging.warning(
                        "No progress made in 3 consecutive iterations. Halting."
                    )
                    break
            else:
                consecutive_no_progress = 0

        logging.info("Refinement finished after %s iteration(s).", actual_iterations)
        return draft


# ========= Main Execution =========

if __name__ == "__main__":
    # Sample execution demonstrating how to use the refactored class
    DEMO_QUESTION = "Explain about LangChain and LangGraph"

    print("=" * 60)
    print(f"QUESTION: '{DEMO_QUESTION}'")
    print("=" * 60)

    # Initialize the class and run the generation
    refiner = IterativeRefiner()
    final_answer = refiner.refine(DEMO_QUESTION, max_iters=10)

    # Output final statistics and results
    final_gaps = final_answer.count(IterativeRefiner.MISSING_MARKER)
    expansion_ratio = len(final_answer) / len(DEMO_QUESTION)

    print("\n" + "=" * 60)
    print("FINAL COMPLETE ANSWER:")
    print("=" * 60)
    print(final_answer)
    print("\n" + "=" * 60)
    print("FINAL STATISTICS:")
    print(f"  - Remaining gaps: {final_gaps}")
    print(f"  - Answer expansion: {expansion_ratio:.1f}x original question length")
    print("=" * 60)
