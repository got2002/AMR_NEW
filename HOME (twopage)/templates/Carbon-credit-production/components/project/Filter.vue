<template>
	<form @submit.prevent="submitForm" class="grid grid-cols-12 gap-2 p-4">
		<div class="xl:col-span-3 lg:col-span-4 md:col-span-6 col-span-12">
			<UILabel :text="$t('project.table.filter.label.status')" />
			<select v-model="filter.status" class="break-words text-sm text-center px-2 py-2 bg-white shadow-sm rounded focus:shadow-sm outline-none w-full border border-gray-200">
				<option value="">{{ $t("project.table.filter.status.all") }}</option>
				<option value="Registered">{{ $t("project.table.filter.status.registered") }}</option>

				<option value="Rejected">{{ $t("project.table.filter.status.rejected") }}</option>
				<option value="Expired">{{ $t("project.table.filter.status.expired") }}</option>
			</select>
		</div>
		<div class="xl:col-span-3 lg:col-span-4 md:col-span-6 col-span-12">
			<UILabel :text="$t('project.table.filter.label.sub_status')" />
			<select v-model="filter.sub_status" class="break-words text-sm text-center px-2 py-2 bg-white shadow-sm rounded focus:shadow-sm outline-none w-full border border-gray-200">
				<option value="">{{ $t("project.table.filter.status.all") }}</option>
				<option value="Pending">{{ $t("project.table.filter.status.pending") }}</option>
				<option value="Certified">{{ $t("project.table.filter.status.certificated") }}</option>
			</select>
		</div>
		<div class="xl:col-span-3 lg:col-span-4 md:col-span-6 col-span-12">
			<UILabel :text="$t('project.table.filter.label.standard')" />
			<select v-model="filter.standard" class="break-words text-sm text-center px-2 py-2 bg-white shadow-sm rounded focus:shadow-sm outline-none w-full border border-gray-200">
				<option value="">{{ $t("project.table.filter.all_standard") }}</option>

				<option value="Standard T-VER">Standard T-VER</option>
				<option value="Premium T-VER">Premium T-VER</option>
				<option value="JCM">JCM</option>
			</select>
		</div>
		<div class="xl:col-span-3 lg:col-span-4 md:col-span-6 col-span-12">
			<UILabel :text="$t('project.table.filter.label.type')" />
			<select v-model="filter.type" class="break-words text-sm text-center px-2 py-2 bg-white shadow-sm rounded focus:shadow-sm outline-none w-full border border-gray-200">
				<option value="">{{ $t("project.table.filter.type") }}</option>
				<option v-for="(project_type, index) in project_types" :value="project_type.abbr" :key="index">{{ project_type[$i18n.locale] }}</option>
			</select>
		</div>
		<div class="xl:col-span-6 lg:col-span-8 col-span-12 relative">
			<UILabel :text="$t('project.table.filter.label.carbon_credit_amount')" />
			<UIRangeSlider ref="slider-range" :min="0" :max="limit.maxTonnes" :minRangeValue="filter.min" :maxRangeValue="filter.max" @setMin="filter.min = Number($event)" @setMax="filter.max = Number($event)" />
		</div>
		<div class="xl:col-span-6 lg:col-span-8 md:col-span-6 col-span-12">
			<UILabel :text="$t('project.table.filter.label.crediting_peroid')" />
			<div class="w-full">
				<DatePicker v-model="filter.vintage" :placeholder="$t('project.view_page.start_date') + ' - ' + $t('project.view_page.end_date')" :lang="$i18n.locale" range format="DD MMM YYYY" :formatter="thaiformatter" value-type="date" input-class="text-sm text-center px-6 py-2.5  bg-white rounded  focus:shadow-sm outline-none w-full border border-gray-200"></DatePicker>
			</div>
		</div>
		<div class="xl:col-span-3 lg:col-span-4 md:col-span-6 col-span-12">
			<UILabel :text="$t('project.table.filter.label.corsia')" />
			<select v-model="filter.authUse" class="break-words text-sm text-center px-2 py-2 bg-white shadow-sm rounded focus:shadow-sm outline-none w-full border border-gray-200">
				<option value="">{{ $t("project.table.filter.all") }}</option>
				<option v-for="(auth, index) in autherizeduses" :value="auth.value" :key="index">{{ auth.text }}</option>
			</select>
		</div>
		<div class="xl:col-span-6 lg:col-span-8 col-span-8">
			<UILabel :text="$t('project.table.filter.search')" />
			<UISearch v-model="filter.searchText" @change="submitForm" :placeholder="$t('project.table.filter.type_to_search')" />
		</div>
		<div class="xl:col-span-3 lg:col-span-4 col-span-4 flex items-end justify-end w-full gap-4 text-sm">
			<UIBackButton @click="$emit('resetFilter')" padding="py-2 px-4" class="text-sm">{{ $t("button.cancel") }}</UIBackButton>
			<input type="submit" :value="$t(`button.apply_filter`)" class="px-4 py-2 bg-tgo-teal-500 hover:bg-tgo-teal-600 shadow-sm rounded text-white flex items-center" />
		</div>
	</form>
</template>

<script>
import thaiformatter from "../../mixins/thaiformatter";
export default {
	props: ["filter", "limit"],
	mixins: [thaiformatter],
	async mounted() {
		await this.getTypes();
		await this.getDropdownAutherizedUse();
	},
	data() {
		return {
			project_types: [],
			autherizeduses: [],
		};
	},

	// updated(){
	//     console.log(this.$refs['slider-range']);
	//     this.$refs['slider-range'].minRangeValue = this.filter.min??0
	//     this.$refs['slider-range'].maxRangeValue = this.filter.max??100000000

	// },
	methods: {
		submitForm(){
			console.log(this.filter.searchText);
			this.$emit('getProject')
		},
		async getTypes() {
			let app = this;
			app.isLoading = true;
			await this.$axios
				.$get(`/api/v1/dropdown/project-types-abbr`)
				.then((resp) => {
					// console.log(resp);
					app.project_types = resp;
				})
				.catch((errors) => {
					console.log(errors);
				});
		},
		async getDropdownAutherizedUse() {
			const app = this;
			await this.$axios
				.$get(`/api/v1/dropdown/authorizeduses`)
				.then((resp) => {
					// console.log(resp);
					app.autherizeduses = resp;
				})
				.catch((errors) => {
					console.log(errors);
				});
		},
	},
};
</script>

<style>
</style>