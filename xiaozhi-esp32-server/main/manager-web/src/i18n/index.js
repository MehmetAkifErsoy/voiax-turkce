import Vue from 'vue';
import VueI18n from 'vue-i18n';
import tr from './tr';

Vue.use(VueI18n);

// Türkçe sürümde arayüz dili sabit olarak Türkçe tutulur.
const getDefaultLanguage = () => {
  const savedLang = localStorage.getItem('userLanguage');
  if (savedLang === 'tr') {
    return savedLang;
  }
  localStorage.setItem('userLanguage', 'tr');
  return 'tr';
};

const i18n = new VueI18n({
  locale: getDefaultLanguage(),
  fallbackLocale: 'tr',
  messages: {
    'tr': tr
  }
});

export default i18n;

// Dil değiştirme çağrıları Türkçe'de kalacak şekilde yönlendirilir.
export const changeLanguage = () => {
  i18n.locale = 'tr';
  localStorage.setItem('userLanguage', 'tr');
  // Bileşenlere dil bilgisinin güncellendiğini bildir.
  Vue.prototype.$eventBus.$emit('languageChanged', 'tr');
};
