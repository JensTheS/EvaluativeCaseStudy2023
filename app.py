from transformers import AutoTokenizer, AutoModelForCausalLM
import json

tokenizer = AutoTokenizer.from_pretrained("codeparrot/codeparrot-small")
model = AutoModelForCausalLM.from_pretrained(
    "codeparrot/codeparrot-small", pad_token_id=tokenizer.eos_token_id
)


def app(environ, start_response):
    # Get the request body from the WSGI environment
    length = int(environ.get("CONTENT_LENGTH", "0"))
    body = environ["wsgi.input"].read(length).decode()

    # Parse the request body as JSON
    request = json.loads(body)

    # Get the input text and maximum number of tokens from the request
    prompt = request["prompt"]
    comment = request["comment"]
    text = f"{prompt}\n{comment}"
    max_tokens = int(
        request.get("max_tokens", 50)
    )  # get max_tokens from request, default to 50 if not specified
    num_return_sequences = int(
        request.get("num_return_sequences", 1)
    )  # get num_return_sequences from request, default to 1 if not specified

    # Run the model on the input text
    inputs = tokenizer(text, return_tensors="pt")

    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        pad_token_id=tokenizer.eos_token_id,
        max_length=inputs["input_ids"].shape[-1] + max_tokens,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        num_return_sequences=num_return_sequences,
    )

    # Convert the model output to JSON and return it
    response = {"output": []}
    for i in range(num_return_sequences):
        output_sequence = outputs[i]
        decoded_output = tokenizer.decode(output_sequence, skip_special_tokens=True)
        response["output"].append(decoded_output)

    response["num_tokens"] = outputs.shape[-1]
    if outputs.shape[-1] == model.config.max_length:
        response["end_of_sequence"] = True

    response_body = json.dumps(response).encode()

    # Set the response headers
    status = "200 OK"
    headers = [
        ("Content-type", "application/json"),
        ("Content-Length", str(len(response_body))),
    ]

    # Call the start_response function to send the headers
    start_response(status, headers)

    # Return the response body
    return [response_body]
