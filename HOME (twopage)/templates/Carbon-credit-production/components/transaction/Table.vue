<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 3xl:overflow-hidden overflow-x-scroll shadow-sm rounded">
		<table class="items-center w-full space-y-6">
			<thead>
				<tr class="bg-tgo-teal-500">
					<template v-for="(header, idx) in table.head">
						<TransactionHeaderSlot :key="idx" :header="header" ></TransactionHeaderSlot>
					</template>
				</tr>
			</thead>
			<tbody class="bg-white">
				<template v-for="(data, index) in project">
					<tr :key="index" :class="{ 'bg-gray-100 hover:bg-gray-200': index % 2 == 1 }" class="focus:outline-none text-xs hover:bg-gray-50 h-10 rounded align-middle">
						<TransactionDataSlot class="w-20" :text="index+1" align="center"></TransactionDataSlot>
						<TransactionDataSlot class="cursor-pointer hover:text-blue-500" :title="projectName(data.project_name)" :text="'#'+data.projectId" align="center"></TransactionDataSlot>
					
						<TransactionNameSlot :userId="data.fromAccountNumber" :name="data.fromAccountName" align="center"></TransactionNameSlot>
						<TransactionNameSlot :userId="data.toAccountNumber" :name="data.toAccountName" align="center"></TransactionNameSlot>
						<TransactionDataSlot :text="data.amount.toLocaleString()" align="center"></TransactionDataSlot>
						
						
						<TransactionStatusSlot :status="data.status" align="center"></TransactionStatusSlot>
						<TransactionDataSlot :text="datetime(data.createdAt)" align="center"></TransactionDataSlot>
						<TransactionActionSlot :status="data.status" :id="data._id" :transferTypeID="data.transferTypeID" :encryptID="data.encrypt_id" @reload="$emit('reload')" :loading="loading"></TransactionActionSlot>
					</tr>
				</template>
			</tbody>
		</table>

		<div v-if="project.length == 0" tabindex="0" colspan="9" class="focus:outline-none text-xs h-16 bg-white rounded hover:bg-theme-green-100 align-middle cursor-pointer">
			<div class="flex justify-center items-center">
				<span class="font-medium text-xs text-theme-black-300 mt-5">{{ $t("alert.no_data") }}</span>
			</div>
		</div>
	</div>
</template>

<script>
	import moment from "moment";
	
	export default {
		
		props: ["project","loading"],
		data() {
			return {
				sort: [0, 0, -1, 0],
				modalOpen: false,
				table: {
					head: [
						{
							name: this.$t("transaction.table.header.no"),
							align: "center",
							filterable: false,
							colspan:1,
							rowspan:1,
						},
						{
							name: this.$t("transaction.table.header.project_id"),
							align: "center",
							filterable: false,
							colspan:1,
							rowspan:1,
						},

						{
							name: this.$t("transaction.table.header.sender"),
							align: "center",
							filterable: false,
							colspan:1,
							rowspan:1,
						},

						{
							name: this.$t("transaction.table.header.receiver"),
							align: "center",
							filterable: false,
							colspan:1,
							rowspan:1,
						},
						{
							name: this.$t("transaction.table.header.amount"),
							align: "center",
							filterable: false,
							colspan:1,
							rowspan:1,
						},

						{
							name: this.$t("transaction.table.header.status"),
							align: "center",
							filterable: false,
							colspan:1,
							rowspan:1,
						},

						{
							name: this.$t("transaction.table.header.date"),
							align: "center",
							filterable: false,
							colspan:1,
							rowspan:1,
						},
						{
							name: "",
							align: "center",
							filterable: false,
							colspan:1,
							rowspan:1,
						},
					],
				},
				selectInfo: {},
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
			openModalEvt(data) {
				this.selectInfo = data;
				this.modalOpen = true;
			},
			statustran(data) {
				if (this.$i18n.locale === "th") {
					switch (data) {
						case "Registered":
							return "ขึ้นทะเบียน";

						case "Cancelled":
							return "ยกเลิก";
						case "Expired":
							return "สิ้นสุดโครงการ";

						case "Certified":
							return "รับรองแล้ว";
						case "Pending":
							return "รอรับรอง";
						default:
							return "null";
					}
				} else {
					switch (data) {
						case "Registered":
							return "Registered";
						case "Certified":
							return "Certified";
						case "Pending":
							return "Pending";
						case "Cancelled":
							return "Cancelled";
						case "Expired":
							return "Expired";
						default:
							return "null";
					}
				}
			},
			projectName(data) {
				if (this.$i18n.locale === "th") {
					return data.thai;
				} else {
					return data.english;
				}
			},
			ccmgm(data) {
				if (this.$i18n.locale === "th") {
					return data;
				} else {
					switch (data) {
						case "พลังงานหมุนเวียนหรือพลังงานที่ใช้ทดแทนเชื้อเพลิงฟอสซิล":
							return "Renewable energy or fossil fuel replacement";
						case "การเพิ่มประสิทธิภาพการผลิตไฟฟ้าและการผลิตความร้อน":
							return "Improvement of the efficiency of electricity and heat generation";
						case "การใช้ระบบขนส่งสาธารณะ":
							return "Use of public transportation system";
						case "การใช้ยานพาหนะไฟฟ้า":
							return "Use of electric vehicle";
						case "การเพิ่มประสิทธิภาพเครื่องยนต์":
							return "Improvement of the efficiency of engine";
						case "การเพิ่มประสิทธิภาพการใช้พลังงานในอาคารและโรงงาน และในครัวเรือน":
							return "Improvement of the efficiency of energy consumption in building and factory and in household";
						case "การปรับเปลี่ยนสารทำความเย็นธรรมชาติ":
							return "Use of natural refrigerant";
						case "การใช้วัสดุทดแทนปูนเม็ด":
							return "Use of clinker substitute";
						case "การจัดการขยะมูลฝอย":
							return "Solid waste management";
						case "การจัดการน้ำเสียชุมชน":
							return "Domestic wastewater management";
						case "การนำก๊าซมีเทนกลับมาใช้ประโยชน์":
							return "Methane recovery and utilization";
						case "การจัดการน้ำเสียอุตสาหกรรม":
							return "Industrial wastewater management";
						case "การลด ดูดซับ และกักเก็บก๊าซเรือนกระจกจากภาคป่าไม้และการเกษตร":
							return "Reduction, absorption and removal of greenhouse gases from the forestry and agriculture sectors";
						case "การดักจับ กักเก็บ และ/หรือใช้ประโยชน์จากก๊าซเรือนกระจก":
							return "Capture, storage, and/or utilization of greenhouse gas";
						default:
							return "Other project specified by the Board of Directors of TGO";
					}
				}
			},
			statusText(data) {
				if (data === "Pending") {
					return this.$t("project.table.status.pending");
				} else if (data === "Rejected") {
					return this.$t("project.table.status.rejected");
				} else if (data === "Verified") {
					return this.$t("project.table.status.verified");
				} else {
					return this.$t("project.table.status.expired");
				}
			},
			// setSortValue() {
			// 	if (this.sort === 0) {
			// 		this.sort = 1;
			// 	} else if (this.sort === 1) {
			// 		this.sort = -1;
			// 	} else {
			// 		this.sort = 0;
			// 	}
			// 	this.$emit("searchKeyup", this.sort);
			// },
			setSortValue(text, value) {
				switch (text) {
					case "project_id":
						if (this.sort[0] === 0) {
							this.sort[0] = 1;
						} else if (this.sort[0] === 1) {
							this.sort[0] = -1;
						} else {
							this.sort[0] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 0) {
								this.sort[i] = 0;
							}
						}
						break;
					case "project_name.thai":
						if (this.sort[1] === 0) {
							this.sort[1] = 1;
						} else if (this.sort[1] === 1) {
							this.sort[1] = -1;
						} else {
							this.sort[1] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 1) {
								this.sort[i] = 0;
							}
						}
						break;
					case "project_name.english":
						if (this.sort[1] === 0) {
							this.sort[1] = 1;
						} else if (this.sort[1] === 1) {
							this.sort[1] = -1;
						} else {
							this.sort[1] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 1) {
								this.sort[i] = 0;
							}
						}
						break;
					case "registration_date":
						if (this.sort[2] === 0) {
							this.sort[2] = 1;
						} else if (this.sort[2] === 1) {
							this.sort[2] = -1;
						} else {
							this.sort[2] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 2) {
								this.sort[i] = 0;
							}
						}
						break;
					case "carbon_credit_total":
						if (this.sort[3] === 0) {
							this.sort[3] = 1;
						} else if (this.sort[3] === 1) {
							this.sort[3] = -1;
						} else {
							this.sort[3] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 3) {
								this.sort[i] = 0;
							}
						}
						break;
					default: {
						if (this.sort[0] === 0) {
							this.sort[0] = 1;
						} else if (this.sort[0] === 1) {
							this.sort[0] = -1;
						} else {
							this.sort[0] = 0;
						}
						for (let i = 0; i < this.sort.length; i++) {
							if (i !== 0) {
								this.sort[i] = 0;
							}
						}
						break;
					}
				}
				this.$emit("searchKeyup", text, this.sort[value]);
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

			dateToString(data) {
				return moment(data).format("YYYY-MM-DD");
			},
			fullname(data) {
				return data.firstname + " " + data.lastname;
			},
			sumCarbon(data) {
				let sum = 0;
				data.forEach((element) => {
					sum += element.amount;
				});
				return sum;
			},
			Onpage(id) {
				this.$router.push(this.localePath({ name: "project-id", params: { id: id } }));
			},
		},
	};
</script>
<style>
	.table-mim-w {
		min-width: 100%;
	}
</style>
