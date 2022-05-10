// Importing Bootstrap forces the load of the type definition for the window.bootstrap global.
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import Bootstrap from 'bootstrap';

// Vendors
import './vendors/choices';

// Behaviors
import './behaviors/input-rut';
import './behaviors/regions';

// Utils
import { App } from './utils/app';

window.addEventListener('DOMContentLoaded', () => {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach((alert) => {
    App.Utils.highlight(alert);
  });

  setTimeout(() => {
    const mainAlerts = document.querySelectorAll('.main-alert .alert');
    mainAlerts.forEach((alert) => {
      window.bootstrap.Alert.getInstance(alert)?.close();
    });
  }, 10000);

  document.querySelectorAll('form')
    .forEach((form) => {
      form.addEventListener('submit', () => {
        const submitButtons = [...form.elements].filter((element) => (
          element.matches('[type="submit"]:not(.js-do-not-disable-on-submit)')
        ));

        // Disable buttons after submit to prevent disabling submit inputs
        // with values
        submitButtons.forEach((submitButton) => {
          // eslint-disable-next-line no-param-reassign
          (submitButton as HTMLButtonElement).disabled = true;
          App.Utils.showLoading(submitButton);
        });

        return true;
      });
    });
});
