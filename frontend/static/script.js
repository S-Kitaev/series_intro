const uploadBox = document.getElementById('uploadBox');
const videoInput = document.getElementById('videoInput');
const videoPreview = document.getElementById('videoPreview');
const findBtn = document.getElementById('findBtn');
const downloadBtn = document.getElementById('downloadBtn');
const resultDiv = document.getElementById('result');

videoInput.addEventListener('click', e => e.stopPropagation());

uploadBox.addEventListener('click', () => videoInput.click());

videoInput.addEventListener('change', () => {
  const file = videoInput.files[0];
  if (file) {
    const url = URL.createObjectURL(file);
    videoPreview.src = url;
    uploadBox.replaceWith(videoPreview);
    videoPreview.hidden = false;
    findBtn.disabled = false;
    resultDiv.textContent = '';
  }
});

findBtn.addEventListener('click', async () => {
  const file = videoInput.files[0];
  if (!file) return;
  findBtn.disabled = true;
  resultDiv.textContent = 'Идёт обработка...';

  const form = new FormData();
  form.append('file', file);

  try {
    const res = await fetch('/detect_intro/', {
      method: 'POST',
      body: form
    });
    if (!res.ok) {
      throw new Error(`Ошибка сервера: ${res.status}`);
    }
    const data = await res.json();
    resultDiv.innerHTML = `<p>Заставка начинается: <strong>${data.start}</strong></p>
                           <p>Заставка заканчивается: <strong>${data.end}</strong></p>`;
  } catch (err) {
    resultDiv.textContent = `Ошибка: ${err.message}`;
  } finally {
    findBtn.disabled = false;
  }
});

downloadBtn.style.display = 'none';