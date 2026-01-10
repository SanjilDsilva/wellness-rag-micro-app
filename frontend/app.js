const askBtn = document.getElementById("askBtn");
const questionInput = document.getElementById("question");
const responseDiv = document.getElementById("response");
const answerText = document.getElementById("answerText");
const sourcesDiv = document.getElementById("sources");

askBtn.addEventListener("click", async () => {
  const question = questionInput.value.trim();
  if (!question) return;

  askBtn.textContent = "Thinking...";
  askBtn.disabled = true;

  try {
    const res = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    const data = await res.json();

    answerText.textContent = data.answer;
    sourcesDiv.innerHTML = "";

    if (data.sources && data.sources.length > 0) {
      const ul = document.createElement("ul");
      data.sources.forEach(s => {
        const li = document.createElement("li");
        li.textContent = `${s.title} — ${s.source}`;
        ul.appendChild(li);
      });
      sourcesDiv.appendChild(ul);
    }

    responseDiv.classList.remove("hidden");
  } catch (err) {
    answerText.textContent = "Something went wrong. Please try again.";
    responseDiv.classList.remove("hidden");
  }

  askBtn.textContent = "Ask";
  askBtn.disabled = false;
});
