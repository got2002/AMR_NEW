<template>
	<div class="bg-gray-200 w-16 h-7 rounded relative cursor-pointer" @click="swicthLang">
		<div class="bg-white w-6 h-6 shadow-sm rounded absolute z-20 top-0.5 left-0.5 transform flex items-center justify-center duration-100 delay-75" :class="{ 'translate-x-0': $i18n.locale == 'th', 'translate-x-9': $i18n.locale == 'en' }">
			<country-flag v-show="$i18n.locale == 'th'" country="th" size="small" />
			<country-flag v-show="$i18n.locale == 'en'" country="gb" size="small" />
		</div>
		<div v-show="$i18n.locale == 'th'" class="absolute z-10 transform translate-x-7 top-0 m-1  text-sm duration-100 delay-100">ไทย</div>
		<div v-show="$i18n.locale == 'en'" class="absolute z-10 transform translate-x-2 top-0 m-1  text-sm duration-100 delay-100">EN</div>
	</div>
</template>

<script>
	export default {
		name: "Language-widget",
		data() {
			return {};
		},
		methods: {
			swicthLang() {
				if (this.$i18n.locale === "th") {
					this.$router.push(this.switchLocalePath("en"));
				} else {
					this.$router.push(this.switchLocalePath("th"));
				}
			},
		},
	};
</script>

<style></style>
