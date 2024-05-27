<template>
	<div v-if="isdata" class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 mt-2">
		<template v-for="(project, idx1) in credit">
			<span :key="idx1 + 'home'" class="font-medium text-sm text-theme-black-300 leading-6 ml-2 py-2"
				><span class="font-bold">{{ $t("account.transfer.project_number") }}</span> {{ project[0].projectId }}</span
			>
			<span :key="idx1 + 'home2'" class="font-medium text-sm text-theme-black-300 leading-6 ml-2 pb-2"
				><span class="font-bold">{{ $t("account.transfer.project_name") }}</span> {{ nameLocale(project[0].project_name) }}</span
			>
			<table :key="idx1" class="items-center w-full space-y-6 border border-theme-black-300">
				<thead>
					<tr>
						<template v-for="(item, idx) in table.head">
							<ApiHeadSlotWhite :text="item.name" :key="idx" :align="item.align" />
						</template>
					</tr>
				</thead>
				<tbody class="bg-white border border-theme-black-300">
					<template v-for="(data, idx2) in project">
						<tr tabindex="0" class="focus:outline-none text-xs h-12 rounded hover:bg-theme-green-100 align-middle border border-theme-black-300" :key="idx2">
							<td width="40%" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
								<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 uppercase">{{ data.year }}</span>
							</td>
							<td width="35%" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
								<!-- <span class="font-medium text-sm text-theme-black-300 leading-6 ml-2 uppercase">{{ data.amount }}</span> -->
								<div class="hidden">{{ togglehidden }}</div>
								<div v-if="!editAmount[idx1][idx2]" class="flex justify-center">
									<span class="font-medium text-sm text-theme-black-300 leading-6 ml-2">{{ data.amount }}</span>
									<button v-if="role == 99" class="flex items-center px-2" @click="toggle(idx1, idx2)">
										<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square text-yellow-500" viewBox="0 0 16 16">
											<path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
											<path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z" />
										</svg>
									</button>
								</div>
								<div v-else class="flex justify-start">
									<input v-if="editAmount[idx1][idx2]" type="text" v-model="data.amount" class="font-medium w-1/2 text-sm border text-theme-black-300 leading-6 ml-2 px-2" />
									<button v-if="editAmount[idx1][idx2]" class="flex items-center px-2" @click="editName(data,idx1, idx2)">
										<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-green-500">
											<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
										</svg>
									</button>
									<button v-if="editAmount[idx1][idx2]" class="flex items-center" @click="cancle(idx1, idx2)">
										<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-red-500">
											<path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
										</svg>
									</button>
								</div>
							</td>
							<td width="35%" class="border-t-0 px-1 align-center whitespace-nowrap justify-center text-center border border-theme-black-300">
								<div class="w-full flex items-center justify-center gap-2">
									<button @click="show(idx1, idx2)" :class="{ 'text-green-500': projectSelect.arr[0] == idx1 && projectSelect.arr[1] == idx2, 'text-blue-500': projectSelect.arr[0] != idx1 || projectSelect.arr[1] != idx2 }">
										<div class="hidden">{{ projectSelect.toggle }}</div>
										<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
											<path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
										</svg>
									</button>
								</div>
							</td>
						</tr>
						<!-- <tr tabindex="0" class="focus:outline-none text-xs h-12 rounded hover:bg-theme-green-100 align-middle border border-theme-black-300" :key="index + 'sum'">
						
					</tr> -->
					</template>
				</tbody>
			</table>
		</template>

		<!-- <modal name="my-first-modal">
			<div class="grid grid-cols-2 gap-4 p-4">
				<div class="col-span-1 flex flex-col">
					<span>ชื่อ-สกุล</span>
					<span class="font-thin text-gray-400">Name</span>
				</div>
				<div class="col-span-1">
					<div class="w-full py-3 text-center">
						<v-select :options="dropdown.users" :reduce="(text) => text.value" label="text" />
					</div>
				</div>
				<div class="col-span-1 flex flex-col">
					<span>จำนวน</span>
					<span class="font-thin text-gray-400">Quantity</span>
				</div>
				<div class="col-span-1">
					<input type="number" :placeholder="'ไม่เกิน' + this.value" class="w-full py-3 text-center border border-gray-300" />
				</div>
			</div>
		</modal> -->
	</div>
</template>

<script>
export default {
	props: ["form", "projectSelect" ,"id"],
	data() {
		return {
			showModal: false,
			dataModal: {},
			value: 0,
			isdata: false,
			credit: [],
			grouped: [],
			editAmount: [],
			number: 0,
			role:1,
			origin: null,
			togglehidden: true,
			dropdown: {
				users: [
					{
						text: "Users",
						value: "users",
					},
					{
						text: "Users2",
						value: "users2",
					},
				],
			},
			table: {
				head: [
					{
						name: this.$t("account.view.year"),
						align: "center",
						filterable: false,
					},
					{
						name: this.$t("account.view.quantity"),
						align: "center",
						filterable: false,
					},
					{
						name: this.$t("account.view.transfer"),
						align: "center",
						filterable: false,
					},
					// {
					// 	name: this.$t("account.view.view"),
					// 	align: "center",
					// 	filterable: false,
					// },
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
		console.log(this.form);
		
		this.role = this.$auth.user.role
		console.log(this.role)
		this.grouped = this._.groupBy(this.form, "projectId");
		for (const [key, value] of Object.entries(this.grouped)) {
			// console.log(`${key}: ${value}`);
			this.credit.push(value);
		}
		console.log(this.credit);
		for (let i = 0; i < this.credit.length; i++) {
			this.editAmount.push([]);
			for (let j = 0; j < this.credit[i].length; j++) {
				this.editAmount[i].push(false);
			}
		}
		this.isdata = true;
	},
	methods: {
		cancle(index1, index2) {
			this.credit[index1][index2].amount = this.origin;
			this.editAmount[index1][index2] = !this.editAmount[index1][index2];
			this.togglehidden = !this.togglehidden;
			// this.$emit("getAccount");
		},
		toggle(index1, index2) {
			for (let i = 0; i < this.editAmount.length; i++) {
				for (let j = 0; j < this.editAmount[i].length; j++) {
					if (this.editAmount[i][j] === true) {
						this.editAmount[i][j] = false;
						this.credit[i][j].amount = this.origin;
					}
				}
			}
			this.origin = this.credit[index1][index2].amount;
			this.editAmount[index1][index2] = !this.editAmount[index1][index2];
			this.togglehidden = !this.togglehidden;
			// this.$emit("getAccount");
		},
		async editName(data,index1,index2) {
			const app = this;
			console.log(data,this.id)
			const form = {
				amount : data.amount,
				projectId : data.projectId,
				vintageId : data._id,
				year : data.year
			};
			await this.$axios
				.$put(`/api/v1/account/update-vintage/${app.id}`, form)
				.then((resp) => {
					console.log(resp);
					app.editAmount[index1][index2] = !app.editAmount[index1][index2];
					app.togglehidden = !app.togglehidden;
					app.$emit("getAccount");
					// app.dropdowns.account_types = resp;
				})
				.catch((err) => {
					console.log(err);
				});
		},
		nameLocale(name) {
			if (this.$i18n.locale === "th") {
				return name.thai;
			}
			return name.english;
		},
		show(index1, index2) {
			this.projectSelect.toggle = !this.projectSelect.toggle;
			if (this.projectSelect.arr[0] === index1 && this.projectSelect.arr[1] === index2) {
				this.projectSelect.arr[0] = -1;
				this.projectSelect.arr[1] = -1;
			} else {
				this.projectSelect.arr[0] = index1;
				this.projectSelect.arr[1] = index2;
			}
		},
		hide() {
			this.$modal.hide("my-first-modal");
		},
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
	},
};
</script>