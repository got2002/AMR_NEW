<template>
	<div class="w-full grid grid-cols-3 border-t border-dashed mt-3">
		<div class="flex items-center border-b-4 border-tgo-teal-500">
			<input @click="value = 1" hidden v-model="value" id="default-radio-1" type="radio" :value="1" class="w-4 h-4 mr-2 bg-tgo-teal-500" />
			<label for="default-radio-1" :class="{ 'bg-tgo-teal-500 hover:bg-tgo-teal-500 text-white': value == 1 }" class="flex items-center justify-center h-14 w-full px-2 py-1 bg-gray-100 hover:bg-gray-200 cursor-pointer text-sm">{{ $t("project.view_page.environmental") }}</label>
		</div>
		<div class="flex items-center border-b-4 border-tgo-teal-500">
			<input @click="value = 2" hidden v-model="value" id="default-radio-2" type="radio" :value="2" class="w-4 h-4 mr-2 bg-tgo-teal-500" />
			<label for="default-radio-2" :class="{ 'bg-tgo-teal-500 hover:bg-tgo-teal-500 text-white': value == 2 }" class="flex items-center justify-center h-14 w-full px-2 py-1 bg-gray-100 hover:bg-gray-200 cursor-pointer text-sm">{{ $t("project.view_page.societal") }}</label>
		</div>
		<div class="flex items-center border-b-4 border-tgo-teal-500">
			<input @click="value = 3" hidden v-model="value" id="default-radio-3" type="radio" :value="3" class="w-4 h-4 mr-2 bg-tgo-teal-500" />
			<label for="default-radio-3" :class="{ 'bg-tgo-teal-500 hover:bg-tgo-teal-500 text-white': value == 3 }" class="flex items-center justify-center h-14 w-full px-2 py-1 bg-gray-100 hover:bg-gray-200 cursor-pointer text-sm">{{ $t("project.view_page.economical") }}</label>
		</div>
		<div v-show="value == 1" class="flex justify-start items-center w-full col-span-3 bg-theme-black-50 bg-opacity-50 px-6 pb-6 text-sm">
			<p class="break-words list-disc list-inside whitespace-pre-line leading-8">
				{{ environmentLang() }}
				<!-- <label class="flex items-center justify-center px-2 py-1 text-sm">{{ form.co_benefit.environment }}</label> -->
			</p>
		</div>
		<div v-show="value == 2" class="flex justify-start items-center w-full col-span-3 bg-theme-black-50 px-6 pb-6 text-sm">
			<p class="break-words list-disc list-inside whitespace-pre-line leading-8">
				{{ societyLang() }}
			</p>
			<!-- <label class="flex items-center justify-center px-2 py-1 text-sm">{{ form.co_benefit.society }}</label> -->
		</div>
		<div v-show="value == 3" class="flex justify-start items-center w-full col-span-3 bg-theme-black-50 px-6 pb-6 text-sm">
			<p class="break-words list-disc list-inside whitespace-pre-line leading-8">
				{{ economyLang() }}
			</p>
			<!-- <label class="flex items-center justify-center px-2 py-1 text-sm">{{ form.co_benefit.economy }}</label> -->
		</div>
	</div>
</template>
<script>
export default {
	props: ["form"],
	data() {
		return {
			value: 1,
		};
	},
	computed: {
		getBenefit(val) {
			return val.split("-");
		},
	},
	mounted() {
		// console.log(this.loggedInUser, this.isAuthenticated)
	},
	methods: {
		economyLang(){
			if (this.$i18n.locale === "th") {
				return this.form.co_benefit.economy
			}
			return this.form.co_benefit_en.economy
		},
		societyLang(){
			if (this.$i18n.locale === "th") {
				return this.form.co_benefit.society
			}
			return this.form.co_benefit_en.society
		},
		environmentLang(){
			if (this.$i18n.locale === "th") {
				return this.form.co_benefit.environment
			}
			return this.form.co_benefit_en.environment
		},
		dateToString(date) {
			const result = new Date(date).toLocaleDateString("th-TH", {
				year: "numeric",
				month: "long",
				day: "numeric",
			});
			return result;
		},
		sumCarbon() {
			let sum = 0;

			this.form.carbon_credit_cert.forEach((element) => {
				sum += element.amount;
			});
			return sum;
		},
	},
};
</script>
