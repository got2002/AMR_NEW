<template>
	<div class="">
		<div class="flex items-center justify-between gap-2 mt-5">
			<div class="2xl:w-1/2 w-2/6">
				<div class="text-sm font-bold">{{ $t("project.view_page.project_developer") }}</div>
			</div>
			<div class="border-2 border-gray-400 2xl:w-1/2 w-4/6 h-14 flex items-center justify-center overflow-y-auto">
				<div class="text-sm text-center w-full">{{ projectDeveloperLang() }} </div>
			</div>
		</div>
		<div class="flex items-center justify-between gap-2 mt-5">
			<div class="2xl:w-1/2 w-2/6">
				<div class="text-sm font-bold">{{ $t("project.view_page.project_owner") }}</div>
			</div>
			<div class="border-2 border-gray-400 2xl:w-1/2 w-4/6 h-14 flex items-center justify-center overflow-y-auto">
				<div class="text-sm text-center w-full">{{ projectOwnerLang() }}</div>
			</div>
		</div>
		<div class="flex items-center justify-between gap-2 mt-5">
			<div class="2xl:w-1/2 w-2/6">
				<div class="text-sm font-bold">{{ $t("project.view_page.external_assessors") }}</div>
			</div>
			<div class="border-2 border-gray-400 2xl:w-1/2 w-4/6 h-14 flex items-center justify-center overflow-x-auto">
				<div class="text-sm text-center w-full">{{ externalAssessorsLang() }}</div>
			</div>
		</div>
		<div class="flex items-center justify-between gap-2 mt-5">
			<div class="2xl:w-1/2 w-2/6">
				<div class="text-sm font-bold">{{ $t("project.view_page.registered_date") }}</div>
			</div>
			<div class="border-2 border-gray-400 2xl:w-1/2 w-4/6 h-14 flex items-center justify-center overflow-x-auto">
				<div class="text-sm text-center w-full">{{ dateLocale(data.registration_date) }}</div>
			</div>
		</div>

		<div class="flex items-center justify-between gap-2 mt-5">
			<div class="2xl:w-1/2 w-2/6">
				<div class="text-sm font-bold">{{ $t( "project.view_page.credit_period_project") }}</div>
			</div>
			<div class="border-2 border-gray-400 2xl:w-1/2 w-4/6 h-14 flex items-center justify-center overflow-x-auto">
				<div class="text-sm text-center w-full">{{ dateLocale(data.valid_start) }} - {{ dateLocale(data.valid_end) }}</div>
			</div>
		</div>
		<div class="flex items-center justify-between gap-2 mt-5">
			<div class="2xl:w-1/2 w-2/6">
				<div class="text-sm font-bold">{{ $t("project.create_page.project_investment") }}</div>
			</div>
			<div class="border-2 border-gray-400 2xl:w-1/2 w-4/6 h-14 flex items-center justify-center overflow-x-auto">
				<div class="text-sm text-center w-full">{{ data.project_investment?.toLocaleString() || "-" }}</div>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		props: ["data"],
		methods: {
			projectDeveloperLang() {
				if (this.$i18n.locale === "th") {
					return this.data.project_developer;
				}
				return this.data.project_developer_en;
			},
			dateLocale(date) {
				if (this.$i18n.locale === "th") {
					return this.$dayjs(date).locale("th").format("DD MMM BBBB");
				}
				return this.$dayjs(date).locale("en").format("DD MMM YYYY");
			},
			datetime(date) {
				if (this.$i18n.locale === "th") {
					return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
				}
				return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
			},
			projectOwnerLang() {
				if (this.$i18n.locale === "th") {
					return this.data.project_owner;
				}
				return this.data.project_owner_en;
			},

			externalAssessorsLang() {
				if (this.data.external_assessors !== undefined && this.data.external_assessors !== null) {
					if (this.$i18n.locale === "th") {
						return this.data.external_assessors;
					}
					return this.data.external_assessors_en;
				} else {
					return "";
				}
			},
		},
	};
</script>

<style></style>
