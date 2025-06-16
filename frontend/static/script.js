// Получаем элементы страницы
const uploadBox = document.getElementById('uploadBox');
const videoInput = document.getElementById('videoInput');
const videoPreview = document.getElementById('videoPreview');
const findBtn = document.getElementById('findBtn');
const downloadBtn = document.getElementById('downloadBtn');

// Останавливаем всплытие клика от input, чтобы не триггерился uploadBox повторно
videoInput.addEventListener('click', e => e.stopPropagation());

// Клик по области загрузки открывает проводник
uploadBox.addEventListener('click', () => videoInput.click());

// При выборе файла показываем превью и активируем кнопку
videoInput.addEventListener('change', () => {
  const file = videoInput.files[0];
  if (file) {
    const url = URL.createObjectURL(file);
    videoPreview.src = url;
    videoPreview.hidden = false;
    findBtn.disabled = false;
  }
});