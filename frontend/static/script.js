const uploadBox = document.getElementById('uploadBox');
const videoInput = document.getElementById('videoInput');
const videoPreview = document.getElementById('videoPreview');
const findBtn = document.getElementById('findBtn');
const downloadBtn = document.getElementById('downloadBtn');

videoInput.addEventListener('click', e => e.stopPropagation());

uploadBox.addEventListener('click', () => videoInput.click());

videoInput.addEventListener('change', () => {
  const file = videoInput.files[0];
  if (file) {
    const url = URL.createObjectURL(file);
    videoPreview.src = url;
    videoPreview.hidden = false;
    findBtn.disabled = false;
  }
});