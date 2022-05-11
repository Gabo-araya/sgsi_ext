window.addEventListener('DOMContentLoaded', () => {
  const favicon = document.querySelector('[rel=icon]') as HTMLLinkElement;
  const img = new Image();

  if (favicon && favicon.href) {
    document.querySelector('.favicon-ok')?.classList.remove('d-none');
    const faviconHrefElement = document.querySelector('.favicon-href');
    if (faviconHrefElement) {
      faviconHrefElement.innerHTML = favicon.href;
    }
  } else {
    document.querySelector('.favicon-not-ok')?.classList.remove('d-none');
  }

  const ogImage = document.querySelector('meta[name="og:image"]') as HTMLMetaElement;

  if (ogImage && ogImage.content) {
    img.onload = function onload() {
      document.querySelector('.ogImage-not-ok')?.classList.add('d-none');
      const loadedImage = this as HTMLImageElement;

      if (loadedImage.width < 1080 || loadedImage.width !== loadedImage.height) {
        document.querySelector('.ogImage-warning')?.classList.remove('d-none');
      } else {
        document.querySelector('.ogImage-ok')?.classList.remove('d-none');
        const ogImageContentElement = document.querySelector('.ogImage-content');
        if (ogImageContentElement) {
          ogImageContentElement.innerHTML = ogImage.content;
        }
      }
    };

    img.src = ogImage.content;

    // in case everything fails
    document.querySelector('.ogImage-not-ok')?.classList.remove('d-none');
  } else {
    document.querySelector('.ogImage-not-ok')?.classList.remove('d-none');
  }
});
