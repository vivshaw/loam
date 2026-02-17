# vivireview

this Claude plugin is _very_ much inspired by [dollspace.gay](https://bsky.app/profile/dollspace.gay)'s [VDD](https://gist.github.com/dollspace-gay/45c95ebfb5a3a3bae84d8bebd662cc25) methodology- specifically, the *Iterative Adversarial Refinement* step and the Sarcasmotron persona it uses. i've found this technique useful for refining code quality, however it is somewhat effortful to use in a non-automated context, and i don't particularly wish to burn a hole in my wallet automating Gemini calls when i'm already paying for Claude.

so, here i make some compromises:
 - workflow runs purely within Claude Code, using a sub-agent
 - doesn't try to handle any of the earlier or later stages of VDD, just adversarial refinement
 - offers two modes: human-in-the-loop (you decide when to stop) and autonomous (the agent detects when the reviewer is hallucinating or churning and stops on its own)

this is probably somewhat less effective than doll's original method, but on the flipside, has the benefit that you can slap it into any Claude Code instance and it "just works" with no additional specialized tooling.

## usage

two commands are available:

- `/vivireview:review` — **human-in-the-loop mode.** runs an adversarial review, shows you the results, and asks if you want to fix and re-review. loops until you say stop.
- `/vivireview:autoreview` — **autonomous mode.** runs the review-fix loop automatically, stopping when the code passes or the reviewer's feedback is no longer useful. capped at 10 iterations.

both commands accept an optional argument to review specific files or paths. if no argument is provided, they review the current git diff.
