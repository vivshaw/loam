- build an eval suite
- multiharnessify it- support Claude/OpenCode/Codex? check out meta:maintaining-project-context
- autonomous mode
- should it be possible to call implement directly? can the agent clear its own context? twould be cool
- hooks- what to do on other platforms?
- remove "real world impact" sections?
- convert decision trees into graph dsl? `systematic-debugging`?
- use an actual test framework for ethos hooks
- remove any optionality, assume whole suite is installed

concerns w/ superpowers
- https://github.com/obra/superpowers/issues/895
- dead code
- too much choice, let's be more opinionated
- https://github.com/obra/superpowers/issues/1518
- forces plan to include the whole implementation, making it kinda useless- it means TDD does not happen, plus why not just implement at that rate?