---
name: howto-code-in-go
description: Use when writing, reviewing, or modifying Go code - covers naming, error handling and wrapping, doc comments, declarations and scope, API and interface design, concurrency and goroutine lifetimes, and table-driven testing
user-invocable: false
---

# Writing Go

## Overview

Go house style, distilled from Google's [Go Style Guide](https://google.github.io/styleguide/go/guide), Google's [Go Best Practices](https://google.github.io/styleguide/go/best-practices), and [Effective Go](https://go.dev/doc/effective_go). Applies whenever writing, reviewing, or modifying Go code.

Five values, in priority order when they conflict:

1. **Clarity** — a reader can tell what the code does and why.
2. **Simplicity** — it reaches the goal the plainest way available.
3. **Concision** — high signal, low noise.
4. **Maintainability** — it can be changed safely later.
5. **Consistency** — it looks like the code around it.

Clarity breaks ties. Consistency loses them, with one exception: inside a single package, matching the neighbors usually beats being right in isolation.

Prefer the least mechanism. Language construct, then standard library, then an existing dependency, then something new — in that order.

## Non-negotiables

- **`gofmt` everything**, generated code included (`format.Source`). Formatting is not a matter of taste in Go.
- **`MixedCaps` and `mixedCaps`**, never underscores. Export decides the case, not the kind of identifier: `MaxRetries`, `maxRetries`.
- **No line-length limit.** Break a line to expose structure, never to hit a column. Never split a URL or a long string literal across lines.
- **Run `go vet` and `go test -race`** before calling work done.

## Naming

A name is read in context, so it should not repeat the context.

- The package name is already a prefix. `bufio.Reader`, not `bufio.BufReader`. `ring.New`, not `ring.NewRing`.
- Drop the receiver from method names. `buf.WriteTo`, not `buf.WriteBufferTo`.
- No `Get` prefix on accessors: `Owner()` and `SetOwner()`.
- Single-method interfaces take the method name plus `-er`: `Reader`, `Stringer`, `Formatter`. Match the canonical signatures for `Read`, `Write`, `Close`, `Flush`, `String`.
- Nouns for functions that return a value, verbs for functions that do something.
- Add a type to a name only to disambiguate siblings: `ParseInt`, `ParseInt64`.
- **Scope sets length.** `i` inside a three-line loop is right; a package-level variable needs a real name. Same concept, same name across parameters and receivers.
- Receiver names are one or two letters and identical across every method on the type.
- **A package named `util`, `helpers`, `common`, or `misc` describes nothing** and collides on import. Name the package for what it provides. If no such name exists, the code belongs somewhere else.
- Test helper packages append `test`: `creditcardtest`. Name test doubles for behavior: `AlwaysCharges`, `AlwaysDeclines`.
- Proto imports get a `pb` suffix and gRPC imports a `grpc` suffix, prefixed by the service: `configpb`, `configgrpc`. Not `xpb`.

## Comments and documentation

See `style:writing-comments` for the general rules. Go-specific:

- Every exported identifier gets a doc comment that starts with its name and reads as a full sentence.
- Comments carry the *why*. The code already carries the *what*.
- **Boost the signal** when code resembles a familiar idiom but isn't: `if err == nil { // if NO error`.
- Document what a caller cannot infer from the signature: which sentinel errors and error types come back, whether a method mutates its receiver or arguments, whether it is safe for concurrent use, and who is responsible for cleanup.
- Context cancellation semantics are assumed. Document only deviations from them.
- A runnable `Example` function in the test file beats a paragraph of prose.

## Errors

- **Return errors; do not also log them.** Logging on the way out double-reports and takes the decision away from the caller.
- **Give errors structure so callers can interrogate them programmatically.** A package-level sentinel (`var ErrNotFound = errors.New("not found")`) for simple cases; a struct type when the caller needs the details. Callers use `errors.Is` and `errors.As` — never string matching.
- Wrap with `%w` when callers may reasonably inspect the chain, `%v` when annotating for humans or crossing a system boundary where the inner error is an implementation detail. Put `%w` last so the chain reads outermost-first: `fmt.Errorf("read config %q: %w", path, err)`.
- **Add only what the caller doesn't already have.** The underlying error usually names the file, the syscall, and the cause. "failed to" is not information.
- Error strings are lowercase with no trailing punctuation, because they get embedded in longer messages.
- Handle the error or return it. An ignored error (`_ = f.Close()`) needs a comment explaining why that's safe.
- **`log.Fatal` in `main` for unrecoverable startup failure. Libraries return errors** — they never exit the process and never let a panic escape their own boundary. Panic is for API misuse and genuinely impossible states.

## Declarations and scope

- `:=` when initializing with a real value; `var x T` when the zero value is the point.
- **Make zero values useful.** `var buf bytes.Buffer` should be ready to write to. Design types so callers rarely need a constructor.
- A nil slice behaves like an empty one for `len`, `range`, and `append`, so declare `var s []T` rather than allocating. Maps must be made before writing, though reading from a nil map is fine.
- Preallocate capacity only when the final size is actually known: `make([]string, 0, len(m))`. Guessing wastes memory.
- **Keep scopes small.** Declare next to first use. Handle the error immediately and return, so the happy path stays unindented at the left margin.
- Reassigning `err` is fine. **Shadowing in an inner scope is a bug factory** — if the outer variable needs the new value, assign to it explicitly rather than redeclaring. Don't shadow standard library package names either.
- Give channel parameters a direction (`<-chan T`, `chan<- T`). It documents ownership and lets the compiler catch mistakes.

## Functions, types, and APIs

- **Keep signatures short.** A long parameter list is hard to read and easy to call wrong. Often it means the function is doing two things.
- For many optional parameters, take an options struct as the last argument: the fields self-document, omitted fields get sensible zero-value defaults, and it grows without breaking callers. Functional options cost real complexity — reach for them only when most callers pass nothing and the API must keep expanding.
- `context.Context` is the first parameter, named `ctx`. Never store one in a struct.
- **Accept interfaces, return concrete types.** Define the interface in the package that consumes it, not next to the implementation.
- Interfaces have one or two methods. A large interface is usually a struct that hasn't admitted it. Don't invent an interface for a single implementation on the theory that tests will need it.
- Use a pointer receiver when the method mutates or the type is large, and keep the choice consistent across every method on the type.
- Named results are for documenting otherwise-ambiguous returns (`(x, y int)`) or for mutation from a `defer`. Bare `return` in a long function hides what's being returned.
- Reach for generics when the logic is genuinely identical across types and an interface can't express it. One caller is not enough.
- Embed to compose behavior, not to fake inheritance. An embedded type's methods run with the embedded value as receiver, not the outer one.

## Concurrency

- "Do not communicate by sharing memory; instead, share memory by communicating." A mutex guarding a small struct is also fine and often simpler. Choose whichever makes ownership obvious.
- **Every goroutine needs an answer to two questions: when does it exit, and who waits for it?** Without both, it leaks. Pass `ctx` and select on `ctx.Done()`.
- `errgroup.Group` or `sync.WaitGroup` for fan-out; a buffered channel as a semaphore to bound concurrency.
- `defer` the unlock or close immediately after a successful acquire. Arguments evaluate at `defer` time, and deferred calls run last-in-first-out.
- Bounded channels surface backpressure. Unbounded queues hide it until memory runs out.

## Testing

See `style:writing-good-tests` for what to test. Go-specific:

- **Table-driven tests with `t.Run` subtests**, and field names in every case literal so a new field doesn't silently shift the data.
- Failure messages state the call, the result, and the expectation: `t.Errorf("Parse(%q) = %v, want %v", in, got, want)`.
- **Assertion helper libraries are not idiomatic Go.** Keep the comparison and the failure message inside the `Test` function. Helpers do setup and cleanup; validation helpers return values instead of taking `*testing.T`.
- Mark real helpers with `t.Helper()` so failures point at the caller, and register teardown with `t.Cleanup`.
- `t.Fatal` when continuing would be meaningless (setup failed). `t.Error` otherwise, so one run reports every failure. **Never call `t.Fatal` from a goroutine other than the test's own** — use `t.Error` and `return`.
- Compare with `cmp.Diff` from `github.com/google/go-cmp`, not `reflect.DeepEqual`. Diffs are readable; booleans aren't.
- Prefer the real transport with a test server over a hand-written fake client. Hand-rolled clients drift from the production one and test nothing.

### Never skip tests

A test that needs an environment variable, credential, or fixture must **fail with a clear message** when it's missing. Early-return guards and `t.Skip` turn a missing dependency into a silent pass, so a green suite stops meaning anything. If a test can't run, it should be red, not invisible.

## When the guide is silent

Match the surrounding file, then the package. Local consistency covers judgment calls — `%s` versus `%v` in an error, buffered versus unbuffered channels — but it does not license line-length rules, assertion frameworks, or copying a local deviation that would widen an exported API or introduce a bug. Those call for cleanup instead.

## Research before guessing

For an unfamiliar module, an unclear API, or a build failure you can't diagnose immediately, dispatch a research agent instead of iterating by trial and error. They run in isolated context and return summaries.

- `core:researcher-internet` for package documentation, module versions, and ecosystem conventions.
- `core:researcher-remote-code` for reading how an external repository actually implements something.
