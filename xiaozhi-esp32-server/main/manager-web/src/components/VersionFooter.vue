<template>
  <div class="copyright">
    <div class="footer-content">
      <span>© 2026 VoiaX Project | Yerel Robotik Zeka Altyapısı</span>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'VersionFooter',
  computed: {
    ...mapState({
      version: state => state.pubConfig.version,
      name: state => state.pubConfig.name,
      beianIcpNum: state => state.pubConfig.beianIcpNum,
      beianGaNum: state => state.pubConfig.beianGaNum,
      year: state => state.pubConfig.year
    })
  },
  mounted() {
    this.$store.dispatch('fetchPubConfig')
  }
}
</script>

<style scoped>
.copyright {
  padding: 10px 0;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.beian-link {
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}

.beian-icon {
  width: 16px;
  height: 16px;
  vertical-align: middle;
}

.beian-text {
  color: #000;
  font-size: 12px;
  vertical-align: middle;
}
</style>