<template>
	<div id="further" class="space-y-2">
		<div class="flex items-center gap-2">
			<input type="radio" :id="id" :name="name" v-model="model.option" :value="value" class="w-5 h-5" />
			<label :for="id">
				{{ label }}
			</label>
		</div>

		<div v-if="model.option === value">
			<v-select :options="dropdowns.transactions" :reduce="(text) => text.value" :label="$i18n.locale" v-model="model.on_behalf_of"> </v-select>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		value: String,
		id: String,
		name: String,
		label: String,
		model: Object,
	},
	data() {
		return {
			dropdowns: {
				transactions: [],
				accounts: [],
			},
		};
	},
	mounted() {
		this.getTransactionTypeDropdowns();
	},
	methods: {
		async getTransactionTypeDropdowns() {
			this.dropdowns.transactions = await this.$axios
				.$get(`/api/v1/dropdown/transaction-types`)
				.then((resp) => resp)
				.catch((err) => console.log(err));
		},
	},
};
</script>

<style>
#further .v-select .vs__dropdown-toggle {
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	background: #fff;
	border-width:1px !important;
	border-style: solid #b5b5b5 !important;

	border-radius: 0px !important;

	display: flex;
	align-items: center;
	padding: 1px !important;
	white-space: normal;
}
</style>