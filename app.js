const vocab = [
  { word: "你好", pinyin: "nǐ hǎo", meaning: "hello" },
  { word: "谢谢", pinyin: "xièxie", meaning: "thank you" },
  { word: "再见", pinyin: "zàijiàn", meaning: "goodbye" }
];

let current = 0;
const card = document.getElementById("flashcard");
const front = card.querySelector(".front");
const back = card.querySelector(".back");

card.addEventListener("click", () => {
  card.classList.toggle("flipped");
});

function renderCard() {
  front.textContent = vocab[current].word;
  back.textContent = `${vocab[current].meaning} (${vocab[current].pinyin})`;
}

function nextCard() {
  current = (current + 1) % vocab.length;
  renderCard();
  card.classList.remove("flipped");
}

function speakWord() {
  const utter = new SpeechSynthesisUtterance(vocab[current].word);
  speechSynthesis.speak(utter);
}

// Quiz logic
const questionEl = document.getElementById("question");
const choicesEl = document.getElementById("choices");

function startQuiz() {
  const q = vocab[Math.floor(Math.random() * vocab.length)];
  questionEl.textContent = `What does '${q.word}' mean?`;

  const options = [q.meaning];
  while (options.length < 3) {
    const r = vocab[Math.floor(Math.random() * vocab.length)].meaning;
    if (!options.includes(r)) options.push(r);
  }
  options.sort(() => Math.random() - 0.5);

  choicesEl.innerHTML = "";
  options.forEach(opt => {
    const btn = document.createElement("button");
    btn.textContent = opt;
    btn.onclick = () => alert(opt === q.meaning ? "✅ Correct!" : "❌ Wrong!");
    choicesEl.appendChild(btn);
  });
}

renderCard();
startQuiz();
