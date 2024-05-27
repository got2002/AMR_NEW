<template>
	<div class="w-full grid grid-cols-3 border-t border-dashed">
		<div class="flex items-center border-b-4 border-tgo-teal-500">
			<input @click="value = 1" hidden v-model="value" id="default-radio-eng-1" type="radio" :value="1" class="w-4 h-4 mr-2 bg-tgo-teal-500" />
			<label for="default-radio-eng-1" :class="{ 'bg-tgo-teal-500 hover:bg-tgo-teal-500 text-white': value == 1 }" class="flex items-center justify-center h-14 w-full px-2 py-1 bg-gray-100 hover:bg-gray-200 cursor-pointer text-sm">{{$t('project.view_page.environmental')}}</label>
		</div>
		<div class="flex items-center border-b-4 border-tgo-teal-500">
			<input @click="value = 2" hidden v-model="value" id="default-radio-eng-2" type="radio" :value="2" class="w-4 h-4 mr-2 bg-tgo-teal-500" />
			<label for="default-radio-eng-2" :class="{ 'bg-tgo-teal-500 hover:bg-tgo-teal-500 text-white': value == 2 }" class="flex items-center justify-center h-14 w-full px-2 py-1 bg-gray-100 hover:bg-gray-200 cursor-pointer text-sm">{{$t('project.view_page.societal')}}</label>
		</div>
		<div class="flex items-center border-b-4 border-tgo-teal-500">
			<input @click="value = 3" hidden v-model="value" id="default-radio-eng-3" type="radio" :value="3" class="w-4 h-4 mr-2 bg-tgo-teal-500" />
			<label for="default-radio-eng-3" :class="{ 'bg-tgo-teal-500 hover:bg-tgo-teal-500 text-white': value == 3 }" class="flex items-center justify-center h-14 w-full px-2 py-1 bg-gray-100 hover:bg-gray-200 cursor-pointer text-sm">{{$t('project.view_page.economical')}}</label>
		</div>
		<div v-if="value == 1" class="flex justify-start items-center w-full col-span-3 bg-theme-black-50 bg-opacity-50 py-4 px-6 text-sm">
			<textarea v-model="form.co_benefit_en.environment" class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-tgo-yellow-500 focus:outline-none" rows="3"></textarea>
		</div>
		<div v-if="value == 2" class="flex justify-start items-center w-full col-span-3 bg-theme-black-50 py-4 px-6 text-sm">
			<textarea v-model="form.co_benefit_en.society" class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-tgo-yellow-500 focus:outline-none" rows="3"></textarea>
		</div>
		<div v-if="value == 3" class="flex justify-start items-center w-full col-span-3 bg-theme-black-50 py-4 px-6 text-sm">
			<textarea v-model="form.co_benefit_en.economy" class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-tgo-yellow-500 focus:outline-none" rows="3"></textarea>
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
			return val.split('-');
		},
	},
	mounted() {
		// console.log(this.loggedInUser, this.isAuthenticated)
	},
	methods: {
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
