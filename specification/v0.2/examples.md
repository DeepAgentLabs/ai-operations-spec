# v0.2 Relationship Examples

These examples are conceptual and do not prescribe JSON fields.

## Sequential retrieval and answer

A Run contains a retrieval Step and an answer Step. The answer Step `depends-on` the retrieval Step. A RAG Retrieval is `observed-in` the retrieval Step, while a Model Interaction is `observed-in` the answer Step. A groundedness Evaluation `evaluates` the answer.

## Parallel research and join

A coordinator Step causes two sibling research Steps. Neither sibling follows the other. A synthesis Step `depends-on` both research Steps, forming a join. The coordinator Agent `delegated-to` two researcher Agents without changing Step containment.

## Retry

A model-call Step contains two Model Interaction attempts with separate identities. The timeout Reliability Event `signals-on` the first attempt. The second attempt follows the first and both refer to one logical activity. Only the second attempt completes successfully.

## Child run and handoff

A planning Run causes a child execution Run. The child has its own containment boundary. Within the child Run, one Agent `handed-off-to` another Agent. The handoff is not represented as Step parentage.
