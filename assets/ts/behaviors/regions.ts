// Vendors
import Choices, { Choice } from 'choices.js';
import { initChoices } from '../vendors/choices';

// Constants
const REGION_SELECT_SELECTOR = '#id_region';
const COMMUNE_SELECT_SELECTOR = '#id_commune';

// Functions
/**
 * Gets the list of communes corresponding to the region with `id` equals to `regionId`.
 */
async function getRegionCommunes(regionId: string) {
  try {
    const regionIdIsInteger = /^\d+$/.test(regionId);

    if (!regionIdIsInteger) {
      throw new Error('regionId is not a positive integer.');
    }

    const communes = await fetch(`/regions/communes/search/?regionId=${regionId}`);

    return await communes.json() as { id: number | '', text: string, selected?: boolean }[];
  } catch {
    return [];
  }
}

/**
 * Replaces the list of communes of `communeChoices`.
 */
async function setCommuneOptions(communeChoices: Choices, regionId: string) {
  const communes = await getRegionCommunes(regionId);

  const communeSelect = communeChoices.passedElement.element;
  const communeSelectPlaceholder = communeSelect.dataset.placeholder;

  if (communeSelectPlaceholder) {
    communes.unshift({
      id: '',
      text: communeSelectPlaceholder,
      selected: true
    });
  }

  await communeChoices.setChoices(communes as unknown[] as Choice[], 'id', 'text', true);
}

// Initialize behavior
window.addEventListener('DOMContentLoaded', () => {
  // Init choices
  const regionSelect = document.querySelector(REGION_SELECT_SELECTOR) as HTMLSelectElement;
  const communeSelect = document.querySelector(COMMUNE_SELECT_SELECTOR) as HTMLSelectElement;

  if (!regionSelect || !communeSelect) return;

  const regionChoices = initChoices(regionSelect);
  const communeSelectPlaceholder = communeSelect.querySelector('option[value=""]')?.textContent;
  const communeChoices = initChoices(communeSelect);

  // Store placeholder as data attribute
  if (communeSelectPlaceholder) {
    communeSelect.dataset.placeholder = communeSelectPlaceholder;
  }

  // Add initial commune options
  setCommuneOptions(communeChoices, regionChoices.getValue(true) as string).catch(() => {});

  // Update commune options whenever the region changes
  regionSelect.addEventListener('change', (choice) => {
    const { detail } = choice as unknown as { detail: { value: string } };
    setCommuneOptions(communeChoices, detail.value).catch(() => {});
  });
});
