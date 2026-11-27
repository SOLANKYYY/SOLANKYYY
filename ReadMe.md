<h1>
  <picture>
    <source media="(max-width: 760px)" srcset="https://raw.githubusercontent.com/SOLANKYYY/SOLANKYYY/main/assets/mixtape/cover-mobile.svg?v=nightmix-1">
    <img width="100%" src="https://raw.githubusercontent.com/SOLANKYYY/SOLANKYYY/main/assets/mixtape/cover.svg?v=nightmix-1" alt="Om Solanki on shuffle. A duck in headphones plays six tracks above Bengaluru at night. The playlist covers search, computer vision, language models, arcade games, full-stack apps and data experiments.">
  </picture>
</h1>

I’m **Om Solanki**, a B.Tech computer science and AI/ML student at Jain University in Bengaluru. I write Python and MATLAB to see what models pick up, then build web apps people can try. Sometimes that means tracing a prediction back to an image. Sometimes it means settling who’s on laundry duty or keeping score in a seven-game arcade.

One of my favourite ways to explore a project is to change one thing and watch what breaks. Ask the same model a different question. Send the camera worker another frame before it finishes the first. Let a flatmate go away for the day and see whose name ends up next to the dishes.

The duck in the headphones reviews my code. Excellent listener. Suspiciously few comments.

[Portfolio](https://solanki-portfolio-v4.vercel.app/) · [LinkedIn](https://www.linkedin.com/in/solanki-om-b89793330/) · [Email](mailto:om.n.solanki49@gmail.com) · [X](https://x.com/Om_solanki49)

[Inside the builds](#inside-the-builds) · [GitHub activity](#github-activity) · [All repositories](#repository-directory)

## Six projects on rotation

<p align="center">
  <a href="https://github.com/SOLANKYYY/signal-desk"><img width="245" src="https://raw.githubusercontent.com/SOLANKYYY/SOLANKYYY/main/assets/mixtape/signal.svg?v=nightmix-1" alt="A1 · Signal Desk. Trace a chat answer back to the report it cites."></a>
  <a href="https://github.com/SOLANKYYY/RetinaBridge"><img width="245" src="https://raw.githubusercontent.com/SOLANKYYY/SOLANKYYY/main/assets/mixtape/retina.svg?v=nightmix-1" alt="A2 · RetinaBridge. See a retinal image beside the model’s heatmap."></a>
  <a href="https://github.com/SOLANKYYY/agrilens-llm-benchmark"><img width="245" src="https://raw.githubusercontent.com/SOLANKYYY/SOLANKYYY/main/assets/mixtape/agrilens.svg?v=nightmix-1" alt="A3 · AgriLens LLM Benchmark. Compare two local models on 2,200 crop records."></a>
  <a href="https://github.com/SOLANKYYY/GameArena"><img width="245" src="https://raw.githubusercontent.com/SOLANKYYY/SOLANKYYY/main/assets/mixtape/gamearena.svg?v=nightmix-1" alt="B1 · GameArena. Play seven arcade games in a team tournament."></a>
  <a href="https://github.com/SOLANKYYY/flat-and-fork"><img width="245" src="https://raw.githubusercontent.com/SOLANKYYY/SOLANKYYY/main/assets/mixtape/flat-fork.svg?v=nightmix-1" alt="B2 · Flat &amp; Fork. Vote on dinner. Hand over today’s laundry turn."></a>
  <a href="https://github.com/SOLANKYYY/frameflow-vision-lab"><img width="245" src="https://raw.githubusercontent.com/SOLANKYYY/SOLANKYYY/main/assets/mixtape/frameflow.svg?v=nightmix-1" alt="B3 · FrameFlow. Skip frames. Add delays. Watch the pipeline respond."></a>
</p>

Pick a sleeve to open the repository. If you like seeing how something works, the field notes take you to a specific image, prediction or test from each build. [Read the six field notes](https://github.com/SOLANKYYY/SOLANKYYY/blob/main/FIELDNOTES.md)

## GitHub activity

<!-- live-profile-stats -->

<picture>
  <source media="(max-width: 760px)" srcset="https://solankyyy-profile-mixtape.vercel.app/api/activity?view=activity&amp;layout=mobile&amp;v=nightmix-1">
  <img width="100%" src="https://solankyyy-profile-mixtape.vercel.app/api/activity?view=activity&amp;layout=wide&amp;v=nightmix-1" alt="Contribution streaks, a 30-day authored commit graph and a 12-week consistency grid. The text version below includes the current figures.">
</picture>

The streak and weekly grid use days with GitHub contributions. The bars count my authored commits on the default branches of my public repositories. Each chart shows its latest complete UTC day.

[Read the current numbers](https://solankyyy-profile-mixtape.vercel.app/api/activity?view=text) · [Open my contribution calendar](https://github.com/SOLANKYYY#js-contribution-activity-description) · [Browse my public commits](https://github.com/search?q=author%3ASOLANKYYY+user%3ASOLANKYYY+is%3Apublic&type=commits)

<details>
<summary>Repository totals and languages</summary>

<picture>
  <source media="(max-width: 760px)" srcset="https://solankyyy-profile-mixtape.vercel.app/api/activity?view=totals&amp;layout=mobile&amp;v=nightmix-1">
  <img width="100%" src="https://solankyyy-profile-mixtape.vercel.app/api/activity?view=totals&amp;layout=wide&amp;v=nightmix-1" alt="Public repository count, stars, forks and primary languages. Exact values are available in the text link above.">
</picture>

</details>

## Inside the builds

### Side A · Models and evidence

**Signal Desk.** I wanted to be able to ask “where did that come from?” and get back to the exact public report behind an answer. The chat uses up to three matching passages. My favourite test gives it a Windows report, asks for Linux evidence, and checks that it leaves the conversation history empty. [Read the chat tests](https://github.com/SOLANKYYY/signal-desk/blob/main/tests/test_chat.py)

**RetinaBridge.** The most interesting part of this research prototype is a screen with four versions of one retinal photograph. The colour overlay shows which areas influenced the model’s grade. The neighbouring black-and-white panel picks out vessel-like shapes with image processing. I trained the model in MATLAB and exported it to ONNX so I could run it in Python. [See the four panels together](https://github.com/SOLANKYYY/RetinaBridge/blob/main/screening-results.png)

**AgriLens LLM Benchmark.** I gave two local language models the same seven soil and weather measurements. On the very first row, DeepSeek guessed apple and Llama guessed pigeon peas. The recorded crop was rice. I kept all 2,200 pairs of answers, so anyone can open a row, read both explanations and decide which clues they missed. [Compare the original predictions](https://github.com/SOLANKYYY/agrilens-llm-benchmark/blob/main/Crop_model_comparison_results.csv)

### Side B · Games and everyday software

**GameArena.** Seven arcade games share one virtual wallet per team. That made balancing the books as interesting as building the games. In a local load test, 50 teams signed in together and played 1,050 games. At the end I could match every team’s balance to the results its players saw. [Read the capacity test](https://github.com/SOLANKYYY/GameArena/blob/master/docs/capacity.md)

**Flat & Fork.** This started with two flatmate questions. What’s for dinner, and whose turn is it to clean up? Residents can vote on a meal and hand over an unfinished chore when someone goes away. The detail I care about is tomorrow morning. Today’s swap lasts for today, and the normal rotation picks up again. [Follow a one-day handover](https://github.com/SOLANKYYY/flat-and-fork/blob/main/MOBILE-PROFILES-HANDOVER.md)

**FrameFlow.** Imagine a camera feeding a worker every tenth frame. What happens when that worker slows down? In the browser simulation, changing one setting from 100 to 400 milliseconds cuts the number of accepted frames from 30 to 15 in the same ten-second run. You can predict the result and check it against the test. [See the scheduling experiment](https://github.com/SOLANKYYY/frameflow-vision-lab/blob/main/tests/test.cjs)

## A few more things to try

| Start with | What to look for |
| --- | --- |
| [Context Lab](https://context-lab-ashen.vercel.app/) | Read a saved Qwen reply, then change the question from a fact about the world to a fact about the supplied text. See when the answer changes. |
| [LungLens](https://github.com/SOLANKYYY/lunglens) | Compare the classical baseline with our team’s PyTorch model. Both saw the same held-out CT images, and the simpler model scored higher in this experiment. |
| [My project campus](https://solanki-portfolio-v4.vercel.app/) | Walk through an isometric version of my portfolio, or open the terminal if you’d rather type your way around. |

I work with **Python, MATLAB, PyTorch and ONNX Runtime** for experiments, and **Flask, Next.js, MongoDB and PostgreSQL** for the apps around them. If you’re building an applied AI tool, a data experiment people can play with, or a slightly too-competitive game, I’d love to hear about it. [Get in touch](mailto:om.n.solanki49@gmail.com)

## Repository directory

<details>
<summary><strong>Machine learning and computer vision</strong> · 11 repositories</summary>

| Repository | What’s inside |
| --- | --- |
| [RetinaBridge](https://github.com/SOLANKYYY/RetinaBridge) | Retinal-image research prototype with five model grades, Grad-CAM heatmaps and a reviewer’s report. |
| [AgriLens LLM Benchmark](https://github.com/SOLANKYYY/agrilens-llm-benchmark) | Compares two local language models on the same 2,200 crop records and publishes their individual answers. |
| [LungLens](https://github.com/SOLANKYYY/lunglens) | Team project comparing a PyTorch CNN with a classical baseline on lung CT images, with results for each class. |
| [Context Lab](https://github.com/SOLANKYYY/context-lab) | Shows 15 saved Qwen responses to factual questions and questions about a supplied statement. |
| [VeraGate](https://github.com/SOLANKYYY/veragate-face-lab) | Lets you move two thresholds and see when an OpenCV face recognizer accepts, flags or rejects a match. |
| [FrameFlow](https://github.com/SOLANKYYY/frameflow-vision-lab) | Simulates frame skipping, processing delays and worker scheduling in a computer-vision pipeline. |
| [TerraSense](https://github.com/SOLANKYYY/terrasense-crop-lab) | Runs a crop classifier in the browser and compares three models on soil and climate measurements. |
| [InboxLens](https://github.com/SOLANKYYY/inboxlens-message-lab) | Classifies SMS messages locally and shows which words influence the spam score. |
| [HomeLens](https://github.com/SOLANKYYY/homelens-housing-lab) | Breaks a housing regression estimate into feature contributions using a synthetic teaching dataset. |
| [TrendScope](https://github.com/SOLANKYYY/trendscope-market-lab) | Fits trends to historical price CSVs and evaluates them on later observations. |
| [Health Predictive Analytics](https://github.com/SOLANKYYY/Health-Predictive-Analytics-using-ODE-Modeling-Machine-Learning) | Models heart-rate recovery with differential equations and explores health classification with logistic regression. |

</details>

<details>
<summary><strong>Security and databases</strong> · 4 repositories</summary>

| Repository | What’s inside |
| --- | --- |
| [Signal Desk](https://github.com/SOLANKYYY/signal-desk) | Links public threat reports, cited chat answers and investigation notes in a Flask and MongoDB workspace. |
| [TraceLens](https://github.com/SOLANKYYY/tracelens-sysmon-lab) | Compares what survives when 384-dimensional Windows event embeddings are compressed to 2, 10 or 50 dimensions. |
| [MongoDB experiments](https://github.com/SOLANKYYY/No_Sql_Mongodb_work) | Collects 18 database labs, from document design and indexes to replication and vector search. |
| [NoSQL Lab](https://github.com/SOLANKYYY/NoSQL_Lab) | Uses Python exercises to classify database systems and match application requirements to storage models. |

</details>

<details>
<summary><strong>Applications and portfolios</strong> · 4 repositories</summary>

| Repository | What’s inside |
| --- | --- |
| [GameArena · Hollow House](https://github.com/SOLANKYYY/GameArena) | A timed tournament arcade with seven virtual-coin games, team balances and an organizer dashboard. |
| [Flat & Fork](https://github.com/SOLANKYYY/flat-and-fork) | Helps flatmates vote on meals, split kitchen duties and hand over a laundry turn when someone is away. |
| [My Portfolio](https://github.com/SOLANKYYY/my-portfolio) | A React portfolio with project screenshots, experiment notes, education and a résumé. |
| [Interactive Portfolio](https://github.com/SOLANKYYY/solanki-portfolio-v4) | A second way to explore my projects through an isometric city and a command-line interface. |

</details>

<details>
<summary><strong>Programming practice and profile</strong> · 3 repositories</summary>

| Repository | What’s inside |
| --- | --- |
| [LeetCode Solutions](https://github.com/SOLANKYYY/LeetCode-Solutions) | Collects my algorithm solutions across arrays, linked lists, dynamic programming and other topics. |
| [Web Boot Camp](https://github.com/SOLANKYYY/Boot_camp_1) | Early HTML exercises recreating a landing page and building a sign-up form. |
| [GitHub Profile](https://github.com/SOLANKYYY/SOLANKYYY) | Holds the animated mixtape, the public GitHub stats renderer and notes from three builds. |

</details>
