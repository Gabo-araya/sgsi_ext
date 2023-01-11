export const App = {
  Utils: class Utils {
    static hideLoading() {
      document.body.classList.remove('wait');
    }

    static thousandSeparator(x: number) {
      return Math.round(x).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    }

    static showLoading(element: Element) {
      document.body.classList.add('wait');

      if (!element.querySelector('.loading-icon')) {
        element.insertAdjacentHTML(
          'beforeend',
          '<span class="fas fa-spinner fa-spin loading-icon" aria-hidden="true"></span>'
        );
      }
    }

    static highlight(element: Element) {
      element.classList.add('highlight');

      setTimeout(() => {
        element.classList.add('dim');
        element.classList.remove('highlight');
      }, 15);

      setTimeout(() => element.classList.remove('dim'), 1010);
    }
  },
};
