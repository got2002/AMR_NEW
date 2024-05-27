<template>
	<div class="w-7/12 border-r-2 pr-4 text-sm">
		<div class="flex justify-between mt-5">
			<div class="flex flex-col justify-center">
				<div class="text-sm font-bold">{{ $t("api.create_page.form.alias_name") }}</div>
			</div>
			<input v-model="form.name" class="border-2 border-gray-400 w-1/2 h-14 flex justify-center px-6 items-center" />
		</div>
		<div class="flex justify-between mt-5">
			<div class="flex flex-col w-1/2 justify-center">
				<div class="text-sm font-bold">{{ $t("api.create_page.form.full_name") }}</div>
			</div>
			<input v-model="form.fullName" class="border-2 border-gray-400 w-1/2 h-14 flex justify-center px-6 items-center" />
		</div>
		<div class="flex justify-between mt-5">
			<div class="flex flex-col w-1/2 justify-center">
				<div class="text-sm font-bold">{{ $t("api.create_page.form.email") }}</div>
			</div>
			<input v-model="form.email" class="border-2 border-gray-400 w-1/2 h-14 flex justify-center px-6 items-center" />
		</div>
		<div class="flex justify-between mt-5">
			<div class="flex flex-col w-1/2 justify-center">
				<div class="text-sm font-bold">{{ $t("api.create_page.form.purpose_description") }}</div>
			</div>
			<input v-model="form.description" class="border-2 border-gray-400 w-1/2 h-14 flex justify-center px-6 items-center" />
		</div>

		<div id="api_account_dropdown" class="flex justify-between mt-5">
			<div class="flex flex-col w-1/2 justify-center">
				<div class="text-sm font-bold">{{ $t("api.create_page.form.account_number") }}</div>
			</div>
			<!-- <v-select :options="dropdown.accountNumber" :reduce="(item) => item.value" label="text" v-model="form.accountNumber" /> -->
			<div class="border-2 border-gray-400 w-1/2 h-14 flex items-center text-sm px-3">
				<UIDropdownSearch v-model="form.accountNumber" :options="dropdown.accountNumber" valueAttr="value" textAttr="text" :searchable="true" />
			</div>
		</div>

		<div class="flex mt-5">
			<div class="flex flex-col w-1/2 justify-start">
				<div class="text-sm font-bold">{{ $t("api.create_page.form.api_permission") }}</div>
			</div>
			<div class="w-1/2">
				<div class="flex items-center mt-2" v-for="permission in dropdown.scopes" :key="permission.value">
					<input v-model="form.scopes" type="checkbox" class="w-8 h-8 mr-2 bg-gray-100 rounded border-gray-300 " :value="permission.value" />
					<div class="flex flex-col justify-center">
						<div class="text-sm font-bold">{{ permission[$i18n.locale] }}</div>
						<!-- <div class="text-sm text-gray-500">{{ permission.description }}</div> -->
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: ["form"],
	data() {
		return {
			dropdown: {
				scopes: [],
				accountNumber: [],
			},
		};
	},
	async mounted() {
		await this.getScope();
		await this.getAccountNumber();
	},
	methods: {
		getScope() {
			const app = this;
			this.$axios.$get(`/api/v1/dropdown/app/scopes`).then((resp) => {
				// console.log(resp);
				app.dropdown.scopes = resp;
			});
		},
		getAccountNumber() {
			const app = this;
			this.$axios.$get(`/api/v1/dropdown/account-numbers`).then((resp) => {
				// console.log(resp);
				app.dropdown.accountNumber = resp;
			});
		},
	},
};
</script>

<style>
#api_account_dropdown .v-select {
	font-family: inherit;
	position: relative;
	width: 50% !important;
}
#api_account_dropdown .v-select .vs__dropdown-toggle {
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	background: #fff;

	border: 2px solid #a3a3a3 !important;

	border-radius: 0px !important;

	display: flex;
	align-items: center;
	padding: 8px 24px 8px 24px !important;
	white-space: normal;
	height: 56px !important;
	width: 100% !important;
}
#api_account_dropdown .vs__selected-options {
	display: flex;
	flex-basis: 100%;
	flex-grow: 1;
	flex-wrap: wrap;
	padding: 0 2px;
	position: relative;
	text-align: center !important;
}
</style>
