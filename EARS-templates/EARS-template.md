# Easy Approach for Requirements syntax Template (EARS template)

Benefits of EARS:

Clarity: Reduces ambiguity and makes requirements easier to understand.
Conciseness: Encourages short, focused requirements.
Testability: The structured format makes it easier to write test cases.
Consistency: Ensures all requirements are written in a similar style.
Reduced Errors: By minimizing ambiguity, EARS helps prevent misinterpretations and costly mistakes.

Keywords:

shall: Used to indicate a mandatory requirement.
should: Indicates a recommended or desirable behavior.
As long as: Introduces state-dependent requirements.
As soon as: Introduces event-driven requirements.
If: Introduces optional feature requirements.
Then: Used in conjunction with "if" for unwanted behavior.

## Ubiquitous

These requirements are always active and define fundamental properties of the system.

Structure: "The <system name> shall <System response>."

Example: "The system shall have a mass of less than 2 kg."

## State-Driven

These requirements are active as long as the system is in a specific state.

Structure: "When <trigger> the <system name> shall <System response>."

Example: "When the user clicks 'Submit', the system shall save the data."

## Event-Driven

These requirements are triggered by specific events.

Structure: "While <in a specific state> the <system name> shall <System response>."

Example: "While the system is in 'Edit Mode', the user shall be able to modify the text."

## Optional Features

These requirements apply only if a specific feature is present.

Structure: "While <in a specific state> the <system name> shall <System response>."

Example: "Where the system has a printing option, the user shall be able to select the paper size."

## Unwanted Behavior (Error/Failure)

These requirements specify how the system should respond to errors or failures.

Structure: "If <trigger> the <system name> shall <System response>."

Example: "If the user enters an incorrect password, the system shall display an error message."

Example: "If communication between client and server is lost, the system shall display an error message."

##### References

- [AWS post](https://repost.aws/articles/AROjWKtr5RTjy6T2HbFJD_Mw/%F0%9F%91%BB-kiro-agentic-ai-ide-beyond-a-coding-assistant-full-stack-software-development-with-spec-driven-ai)
- [KIRO specs](https://kiro.dev/docs/specs/best-practices/)
- [EARS: The Easy Approach to Requirements Syntax](https://medium.com/paramtech/ears-the-easy-approach-to-requirements-syntax-b09597aae31d)
