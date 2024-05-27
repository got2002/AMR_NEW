<template>
	<div class="w-full space-y-2 mt-2">
		<div class="flex items-center flex-wrap gap-4 text-sm my-4">
			<div class="flex gap-1 items-center">
				<div class="w-5 h-5 bg-yellow-500"></div>
				{{ statusText(0) }}
			</div>
			<!-- <div class="flex gap-1 items-center">
				<div class="w-5 h-5 bg-purple-500"></div>
				{{ statusText(1) }}
			</div> -->
			<div class="flex gap-1 items-center">
				<div class="w-5 h-5 bg-green-500"></div>
				{{ statusText(2) }}
			</div>
			<div class="flex gap-1 items-center">
				<div class="w-5 h-5 bg-red-500"></div>
				{{ statusText(3) }}
			</div>
		</div>
		<div class="divide-y">
			<template v-for="(item, idx) in form.carbon_credit_cert">
				<ProjectTreeList :item="item" :key="idx" :programID="form.programID" :project_id="form.project_id" :authorizedUse="form.authorizedUse" :additionalCertificationCode="form.additionalCertificationCode" :projectStandard="form.standard" :projectTypeByExtens="form.project_type_by_extens"/>
			</template>
		</div>
	</div>
</template>

<script>
export default {
	props: ["form"],
	data() {
		return {
			showModal: false,
			dataModal: {},
			number: 0,
			table: {
				head: [
					{
						name: this.$t("project.view_page.credit_period"),
						align: "center",
						filterable: false,
					},
					{
						name: this.$t("project.view_page.approved_carbon_credits"),
						align: "center",
						filterable: false,
					},
					{
						name: this.$t("project.view_page.greenhouse_gases_amount_approve"),
						align: "center",
						filterable: false,
					},
				],
			},
		};
	},
	computed: {
		// fullName() {
		// 	return `${this.loggedInUser.firstname} ${this.loggedInUser.lastname}`;
		// },
	},
	mounted() {
		// console.log(this.loggedInUser, this.isAuthenticated)
	},
	methods: {
		seePdf(value) {
			// console.log(value);
			this.dataModal = value;
			this.showModal = true;
		},
		dateToString(date) {
			const result = new Date(date).toLocaleDateString("th-TH", {
				year: "numeric",
				month: "long",
				day: "numeric",
			});
			return result;
		},
		dateLocale(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},

		sumCarbon() {
			let sum = 0;
			// console.log(this.form);
			this.form.carbon_credit_cert.forEach((element) => {
				sum += element.amount;
			});
			return sum.toLocaleString();
		},

		statusText(val) {
			switch (val) {
				case 0:
					if (this.$i18n.locale === "th") return "รอการรับรอง";
					else return "Waiting";
				case 1:
					if (this.$i18n.locale === "th") return "กำลังประมวลผล";
					else return "In Progress";
				case 2:
					if (this.$i18n.locale === "th") return "รับรองแล้ว";
					else return "Issued";
				case 3:
					if (this.$i18n.locale === "th") return "ยกเลิกแล้ว";
					else return "Cancelled";
			}
		},
	},
};
</script>