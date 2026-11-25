# Field notes

Three short stops inside my projects. Each starts with something you can check for yourself.

[Signal Desk](#signal-desk) · [RetinaBridge](#retinabridge) · [AgriLens](#agrilens) · [Back to my profile](https://github.com/SOLANKYYY)

## Signal Desk

### Where does a citation come from?

Follow one imported report. Signal Desk splits its text into overlapping passages and stores the original URL with each one. When you ask a question, the app ranks passages that match the selected filters and gives the model up to three. The interface returns the sources alongside the answer. [Follow the retrieval steps](https://github.com/SOLANKYYY/signal-desk/blob/main/docs/ARCHITECTURE.md#assistant-data-flow)

<details>
<summary><strong>What happens if the filter rules out the evidence?</strong></summary>

One test asks for Linux evidence when the test collection contains only a Windows report. The app returns an error, and the test checks that the chat history is still empty. The next test follows a successful answer into storage and checks that its citation still points to the original advisory. [Read the two test cases](https://github.com/SOLANKYYY/signal-desk/blob/main/tests/test_chat.py)

</details>

## RetinaBridge

### What does the bright patch mean?

In the bottom-left image, the warm colours show which regions contributed to the model’s chosen grade. The black-and-white panel beside it comes from a separate image-processing step that highlights vessel-like structures. Comparing both with the original photograph helps explain what each view measures.

<a href="https://github.com/SOLANKYYY/RetinaBridge/blob/main/screening-results.png"><img src="https://raw.githubusercontent.com/SOLANKYYY/RetinaBridge/main/screening-results.png" alt="RetinaBridge results screen showing the original retinal photograph, enhanced input, coloured Grad-CAM overlay and black-and-white vessel-candidate mask" width="550"></a>

This research prototype leaves interpretation to the reviewer. The deployed Python file contains both calculations, in `gradcam_map` and `vessel_candidates`. [Read the inference code](https://github.com/SOLANKYYY/RetinaBridge/blob/deploy-onnx/inference.py)

## AgriLens

### Apple or pigeon peas?

For the first record, DeepSeek-R1 1.5B and Llama 3.2 3B received the same seven measurements. Soil pH was about 6.50 and humidity was about 82%. DeepSeek answered **apple**. Llama answered **pigeon peas**. Both supplied a reason.

<details>
<summary><strong>Reveal the dataset label and the scores</strong></summary>

The label was **rice**. On the next record the models agreed on **chickpea**. That row was labelled **rice** too.

| Model | Correct crop labels out of 2,200 | Accuracy |
| --- | ---: | ---: |
| DeepSeek-R1 1.5B | 83 | 3.77% |
| Llama 3.2 3B | 92 | 4.18% |

I counted matches after trimming spaces and ignoring case. Keeping the original replies makes it possible to inspect a confident mistake one row at a time. [See the saved predictions](https://github.com/SOLANKYYY/agrilens-llm-benchmark/blob/main/Crop_model_comparison_results.csv) · [Read the benchmark method](https://github.com/SOLANKYYY/agrilens-llm-benchmark/blob/main/REPORT.md)

</details>

[Browse all my public repositories](https://github.com/SOLANKYYY/SOLANKYYY/blob/main/ReadMe.md#repository-directory)
