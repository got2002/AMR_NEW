<template>
	<div class="py-4 w-full space-y-4 divide-y bg-white p-4 shadow-sm rounded" v-if="!isResetFilter">
		<div class="grid grid-cols-12 gap-4">
			<div class="lg:col-span-6 col-span-12">
				<UILabel :text="$t('showroom.filter.search')" />
				<UISearch v-model="filter.search" />
			</div>

			<div class="lg:col-span-6 col-span-12">
				<UILabel :text="$t('showroom.filter.availability') + ' (tCO2e)'" />

				<UIRangeSlider :min="0" :max="limit.maxAvailable" :minRangeValue="filter.availability.min" :maxRangeValue="filter.availability.max" @setMin="filter.availability.min = Number($event)" @setMax="filter.availability.max = Number($event)" />
			</div>
			<div class="lg:col-span-4 col-span-8">
				<UILabel :text="$t('showroom.filter.project_type')" />
				<UIDropdown :option="dropdowns.projectType" valueAttr="abbr" :labelAttr="$i18n.locale" v-model="filter.projectType" />
			</div>
			<div class="lg:col-span-2 col-span-4">
				<UILabel :text="$t('showroom.filter.vintage_year')" />
				<div class="w-full">
					<DatePicker v-model="filter.vintageYear" :lang="$i18n.locale" placeholder="YYYY" :formatter="yearFormat" type="year" value-type="date" input-class="px-4 py-2 bg-white w-full border border-gray-300 rounded outline-none  focus:border-green-500 text-center"> </DatePicker>
				</div>
			</div>
			<div class="lg:col-span-6 col-span-12">
				<UILabel :text="$t('showroom.filter.price') + ` (${$t('unit.baht')})`" />

				<UIRangeSlider :min="0" :max="limit.maxPrice" :minRangeValue="filter.priceRange.min" :maxRangeValue="filter.priceRange.max" @setMin="filter.priceRange.min = Number($event)" @setMax="filter.priceRange.max = Number($event)" />
			</div>

			<div class="2xl:col-span-4 xl:col-span-6 col-span-8">
				<UILabel :text="$t('showroom.filter.co_benefit.label')" />

				<ShowroomCobenefitFilter :filter="filter" />
			</div>
			<div class="2xl:col-span-4 xl:col-span-2 col-span-2"></div>
			<div class="2xl:col-span-4 xl:col-span-4 col-span-2 flex items-end justify-end gap-2">
				<button @click="resetFilter" class="px-4 py-2 bg-gray-300 shadow-md rounded text-sm flex items-center justify-center gap-2">
					<IconReturn />
					{{ $t("button.reset") }}
				</button>
				<button @click="$emit('fetch', filter)" class="px-4 py-2 bg-tgo-teal-500 shadow-md rounded text-sm text-white flex items-center justify-center gap-2">
					<IconFilter />
					{{ $t("button.search") }}
				</button>
			</div>
		</div>
		<!-- <div class="w-full flex items-center justify-end pt-4">
			<div class="flex items-end gap-2">
				<button @click="resetFilter" class="px-4 py-2 bg-gray-300 shadow-md rounded text-sm">{{ $t("button.reset") }}</button>
				<button @click="$emit('fetch', filter)" class="px-4 py-2 bg-tgo-teal-500 shadow-md rounded text-sm text-white">{{ $t("button.apply_filter") }}</button>
			</div>
		</div> -->
	</div>
</template>

<script>
import thaiformatter from "../../mixins/thaiformatter";
export default {
	mixins: [thaiformatter],
	props: ["limit", "filter"],
	data() {
		return {
			openAvailabilityConfig: false,
			openPriceRangeConfig: false,

			dropdowns: {
				coBenefit: [
					{ value: "env", text: "ENV" },
					{ value: "social", text: "SOCIAL" },
					{ value: "eco", text: "ECO" },
				],
				projectType: [],
			},
			isResetFilter: false,
		};
	},
	// computed: {
	// 	limit.maxPrice() {
	// 		return this._.maxBy(this.project, (item) => item.price.max)?.price.max;
	// 	},

	// 	limit.maxAvailable() {
	// 		return this._.maxBy(this.project, (item) => item.availableTonne)?.availableTonne;
	// 	},
	// },
	mounted() {
		this.filter.availability.min = 0;
		this.filter.availability.max = Number(this.limit.maxAvailable);

		this.filter.priceRange.min = 0;
		this.filter.priceRange.max = Number(this.limit.maxPrice);
		this.getProjectTypes();
	},
	methods: {
		resetFilter() {
			this.isResetFilter = true;
			this.filter.projectType = "";

			this.filter.vintageYear = "";
			this.filter.availability.min = 0;
			this.filter.availability.max = Number(this.limit.maxAvailable);

			this.filter.priceRange.min = 0;
			this.filter.priceRange.max = Number(this.limit.maxPrice);

			this.filter.coBenefit = [];
			this.$emit("fetch", this.filter);
			setTimeout(() => {
				this.isResetFilter = false;
			}, 100);
		},

		async getProjectTypes() {
			let app = this;
			await this.$axios
				.$get(`/api/v1/dropdown/project-types-abbr`)
				.then((resp) => {
					// console.log(resp);
					app.dropdowns.projectType = resp;
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