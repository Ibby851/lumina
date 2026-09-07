    const composerToggle = document.getElementById('composerToggle');
    const composerPanel = document.getElementById('composerPanel');
    const composerClose = document.getElementById('composerClose');
    const composerCancel = document.getElementById('composerCancel');
    const mediaPreview = document.getElementById('mediaPreview');

    function toggleComposer() {
      composerPanel.classList.toggle('open');
    }

    function previewSelectedFile(input) {
      const file = input.files && input.files[0];
      if (!file) {
        mediaPreview.classList.remove('visible');
        mediaPreview.innerHTML = '';
        return;
      }

      const objectUrl = URL.createObjectURL(file);
      mediaPreview.innerHTML = '';

      if (file.type.startsWith('image/')) {
        const img = document.createElement('img');
        img.src = objectUrl;
        img.alt = 'Uploaded preview';
        mediaPreview.appendChild(img);
      } else if (file.type.startsWith('video/')) {
        const video = document.createElement('video');
        video.src = objectUrl;
        video.controls = true;
        video.autoplay = false;
        mediaPreview.appendChild(video);
      } else if (file.type.startsWith('audio/')) {
        const audio = document.createElement('audio');
        audio.src = objectUrl;
        audio.controls = true;
        audio.style.width = '100%';
        mediaPreview.appendChild(audio);
      }

      mediaPreview.classList.add('visible');
    }

    document.getElementById('audioUpload').addEventListener('change', function () {
      previewSelectedFile(this);
    });

    document.getElementById('videoUpload').addEventListener('change', function () {
      previewSelectedFile(this);
    });

    document.getElementById('imageUpload').addEventListener('change', function () {
      previewSelectedFile(this);
    });

    composerToggle.addEventListener('click', toggleComposer);
    composerClose.addEventListener('click', toggleComposer);
    composerCancel.addEventListener('click', toggleComposer);