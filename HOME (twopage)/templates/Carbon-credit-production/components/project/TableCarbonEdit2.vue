<template>
	<div class="w-full space-y-2 mt-2">
		<div class="flex items-center flex-wrap gap-4 text-sm my-4">
			<div class="flex gap-1 items-center">
				<div class="w-5 h-5 bg-yellow-500"></div>
				{{ statusText(0) }}
			</div>
			<div class="flex gap-1 items-center">
				<div class="w-5 h-5 bg-purple-500"></div>
				{{ statusText(1) }}
			</div>
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
				<ProjectTreeList2 :item="item" :key="idx" :programID="form.programID" :project_id="form.project_id" :authorizedUse="form.authorizedUse" :additionalCertificationCode="form.additionalCertificationCode" :projectStandard="form.standard" :projectTypeByExtens="form.project_type_by_extens" @reload="$emit('reload')"></ProjectTreeList2>
			</template>
		</div>
	</div>
</template>

<script>
import thaiformatter from "../../mixins/thaiformatter";
export default {
	props: ["form", "edit"],
	mixins: [thaiformatter],
	data() {
		return {
			showModal: false,
			index: 0,
			creditPeriod: [],
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
		// console.log(this.creditPeriod);
	},

	methods: {
		uploadSuccess(response, idx) {
			this.form.carbon_credit_cert[idx].certified_files.push(response);
		},

		periodChange(idx) {
			[this.form.carbon_credit_cert[idx].start_date, this.form.carbon_credit_cert[idx].end_date] = this.creditPeriod[idx];
			if (this.creditPeriod[idx].length === 2 && !this.creditPeriod[idx].includes(null)) {
				this.form.carbon_credit_cert[idx].valid_start = this.$dayjs(this.form.carbon_credit_cert[idx].valid_start).format("YYYY-MM-DD");
				this.form.carbon_credit_cert[idx].valid_end = this.$dayjs(this.form.carbon_credit_cert[idx].valid_end).format("YYYY-MM-DD");
			} else {
				this.form.carbon_credit_cert[idx].valid_start = null;
				this.form.carbon_credit_cert[idx].valid_end = null;
			}

			// console.log(this.form.carbon_credit_cert[idx]);
		},
		deletePDF(index) {
			this.form.carbon_credit_cert.splice(index, 1);
		},
		seePdf(value, index) {
			// console.log(value);
			this.index = index;
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
		datetime(date) {
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
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
