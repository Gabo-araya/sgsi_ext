// Vendors
import Choices from 'choices.js';

// Utils
import { getParentBySelector } from '../utils/traversing';

// Constants
const CHOICES_LANG_TEXTS = {
  en: {
    loadingText: 'Loading...',
    noResultsText: 'No results found',
    noChoicesText: 'No choices to choose from',
    itemSelectText: '',
    addItemText: (value: string) => `Press Enter to add <b>"${value}"</b>`,
    maxItemText: (maxItemCount: number) => `Only ${maxItemCount} values can be added`,
    searchPlaceholderValue: 'Search'
  },
  es: {
    loadingText: 'Cargando...',
    noResultsText: 'No se encontraron resultados',
    noChoicesText: 'No hay opciones para elegir',
    itemSelectText: '',
    addItemText: (value: string) => `Pressione Enter para agregar <b>"${value}"</b>`,
    maxItemText: (maxItemCount: number) => `Sólo se pueden agregar ${maxItemCount} valores`,
    searchPlaceholderValue: 'Buscar'
  }
};

const SELECT_VALID_CLASS = 'is-valid';
const SELECT_INVALID_CLASS = 'is-invalid';

const CHOICES_VALID_CLASS = SELECT_VALID_CLASS;
const CHOICES_INVALID_CLASS = SELECT_INVALID_CLASS;

// Functions
/**
 * Define if the placeholder should is visible to the user or not.
 * If `choices` has selected options, then hide it. Otherwise, show it.
 * @param {Choices} choices
 */
function setChoicesMultiplePlaceholderVisibility(choices: Choices) {
  const searchInput = choices.input.element;
  const hasSelectedOptions = (choices.getValue() as []).length !== 0;

  if (hasSelectedOptions) {
    searchInput.classList.add('choices__input--placeholder-hidden');
  } else {
    searchInput.classList.remove('choices__input--placeholder-hidden');
  }
}

/**
 * Initialize `select` element as a Choices
 * @returns {Choices}
 */
export function initChoices(select: HTMLSelectElement) {
  const documentLang = document.documentElement.lang as 'en' | 'es';
  const isMultiple = select.hasAttribute('multiple');
  const placeholder = select.querySelector('option[value=""]')?.textContent;
  const options = {
    shouldSort: false,
    searchResultLimit: 100,
    removeItemButton: isMultiple,
    placeholderValue: '',
    allowHTML: false,
    callbackOnInit: function onInit() {
      const { containerOuter } = this as unknown as { containerOuter: { element: Element } };
      const choicesElement = containerOuter.element;
      const selectHasInvalidClass = select.classList.contains(SELECT_INVALID_CLASS);
      const selectHasValidClass = select.classList.contains(SELECT_VALID_CLASS);
      const selectIsInvalid = select.matches(':invalid');
      const selectIsValid = select.matches(':valid');
      const selectIsInValidatedElement = !!getParentBySelector(choicesElement, '.was-validated');

      if (selectHasInvalidClass || (selectIsInValidatedElement && selectIsInvalid)) {
        choicesElement.classList.add(CHOICES_INVALID_CLASS);
      } else if (selectHasValidClass || (selectIsInValidatedElement && selectIsValid)) {
        choicesElement.classList.add(CHOICES_VALID_CLASS);
      }

      if (selectIsInValidatedElement) {
        select.addEventListener('change', () => {
          if (select.matches(':invalid')) {
            choicesElement.classList.add(CHOICES_INVALID_CLASS);
            choicesElement.classList.remove(CHOICES_VALID_CLASS);
          } else {
            choicesElement.classList.add(CHOICES_VALID_CLASS);
            choicesElement.classList.remove(CHOICES_INVALID_CLASS);
          }
        });
      }
    },
    ...CHOICES_LANG_TEXTS[documentLang]
  };
  const choices = new Choices(select, options);

  // Hide placeholder if select has selected options
  if (isMultiple && placeholder) {
    setChoicesMultiplePlaceholderVisibility(choices);
    select.addEventListener('change', () => {
      setChoicesMultiplePlaceholderVisibility(choices);
    }, false);
  }

  return choices;
}

// Initialize behavior
window.addEventListener('DOMContentLoaded', () => {
  const choicesSelects = document.querySelectorAll('select:not(.js-not-choices):not(#id_region):not(#id_commune)');

  choicesSelects.forEach((v) => initChoices(v as HTMLSelectElement));
});
