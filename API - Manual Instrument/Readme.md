# What I do
- Adding spans for each method 
- creating custom metrics see DT_OTEL_Manual, WSN controller




### personal notes

1. Difference span implementation
    ```
    with self.tracer.start_as_current_span("login()") as span: #NOTE OTEL traces
    with self.tracer.start_as_current_span("login2()") as span: #NOTE OTEL traces
    ```

    vs 

    ```
    with self.tracer.start_as_current_span("login()") as parents: #NOTE OTEL traces
        with self.tracer.start_as_current_span("login2()") as kids: #NOTE OTEL traces
    ```

    same thing if difference class/method. But if in the same method best using parents-kids for accesible 

2. put attributes for simplyfing number of metrics (may can save licensing also, depends on licensing of type APM). so dont need create multiple queueGauge 

    example
    ```
    attributes = {"action": span.name} #this neeeded
    queueGauge.set(len(sql),attributes=attributes)
    ```

