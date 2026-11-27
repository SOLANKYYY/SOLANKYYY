# Field notes

Six short stops inside my projects. Each starts with something you can check for yourself.

**Side A** [Signal Desk](#signal-desk) · [RetinaBridge](#retinabridge) · [AgriLens](#agrilens)

**Side B** [GameArena](#gamearena) · [Flat & Fork](#flat-and-fork) · [FrameFlow](#frameflow)

[Back to my profile](https://github.com/SOLANKYYY)

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

## GameArena

### Do the coins still add up?

Picture fifty teams finishing a game at the same time. A fast response is only part of the job. The result on each team’s screen needs to agree with the wallet and game count stored in PostgreSQL.

| Local test | What I checked at the finish |
| --- | --- |
| 50 teams played one game apiece in each of 21 waves | All 1,050 games completed. Each team’s final balance and play count matched the results returned to its players. |
| One account submitted eight overlapping Dice plays | The final balance, number of games and sequence number used to generate the results all matched. |

The second run gives eight requests a reason to touch the same wallet. That made it a good companion to the fifty-team run, where each team had its own. [Read the setup and measurements](https://github.com/SOLANKYYY/GameArena/blob/master/docs/capacity.md)

## Flat and Fork

### Who has the dishes tomorrow?

Say you’ve finished one chore and still have another on the board when you leave for the day. Mark yourself away and hand the unfinished job to a flatmate who’s home. The finished chore keeps your name in the history, so credit stays with whoever actually did it.

Coming home early leaves the day’s handover in place. Tomorrow the normal rotation resumes. The difference between those two moments is exactly what I wanted to capture when I added away status. [See the handover rules and worked checks](https://github.com/SOLANKYYY/flat-and-fork/blob/main/MOBILE-PROFILES-HANDOVER.md)

## FrameFlow

### Can a worker catch the next frame?

Set the simulated camera to **30 frames per second** and send every **tenth** frame to a single worker. That gives it a new frame roughly every 333 milliseconds. Guess how many it will accept in ten seconds before you look at the table.

| Processing time per frame | Accepted | Dropped while busy |
| --- | ---: | ---: |
| 100 ms | 30 | 0 |
| 400 ms | 15 | 15 |

At 400 milliseconds the next frame arrives while the worker is still busy. By the following arrival it is free again. You can trace that pattern in the simulator or read the assertions for those exact settings. [Explore the scheduling logic](https://github.com/SOLANKYYY/frameflow-vision-lab/blob/main/docs/logic.js) · [Read the tests](https://github.com/SOLANKYYY/frameflow-vision-lab/blob/main/tests/test.cjs)

[Browse all my public repositories](https://github.com/SOLANKYYY/SOLANKYYY/blob/main/ReadMe.md#repository-directory)
