# vivireview

this Claude plugin is _very_ much inspired by [dollspace.gay](https://bsky.app/profile/dollspace.gay)'s [VDD](https://gist.github.com/dollspace-gay/45c95ebfb5a3a3bae84d8bebd662cc25) methodology- specifically, the *Iterative Adversarial Refinement* step and the Sarcasmotron persona it uses. i've found this technique useful for refining code quality, however it is somewhat effortful to use in a non-automated context, and i don't particularly wish to burn a hole in my wallet automate Gemini calls when i'm already paying for Claude.

so, here i make some compromises:
 - workflow runs purely within Claude Code, using a sub-agent
 - doesn't try to handle any of the earlier or later stages of VDD, jsut adversarial refinement
 - replaces automated hallucination-based termination with human-in-the-loop- the plugin will continue iterating until you, the user, tell it to stop

this is probably somewhat less effective than doll's original method, but on the flipside, has the benefit that you can slap it into any Claude Code instance and it "just works" with no additional specialized tooling.
