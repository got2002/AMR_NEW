<template>
	<div class="w-full grid grid-cols-1 xl:grid-cols-1 2xl:grid-cols-1 4xl:overflow-hidden overflow-x-scroll shadow-sm rounded">
		<table class="items-center w-full space-y-6">
			<thead>
				<tr class="bg-tgo-teal-500">
					<template v-for="(header, idx) in tHead">
						<UserHeaderSlot :header="header" :key="idx" @setSort="setSort(header.sortKey, $event, idx)" />
					</template>
				</tr>
			</thead>
			<tbody class="bg-white">
				<template v-for="(data, index) in tData">
					<tr tabindex="0" :class="{ 'bg-gray-100': index % 2 == 1 }" class="text-xs h-10 rounded hover:bg-theme-green-100 align-middle" :key="index">
						<!-- <UserDataSlot :text="index + 1" align="center"></UserDataSlot> -->
						<UserDataSlot :text="fullname(data)" align="left"></UserDataSlot>
						<UserDataSlot :text="data.email" align="left"></UserDataSlot>
						<UserDataSlot :text="data.organization || '-'" align="left"></UserDataSlot>
						<UserDataSlot :text="userRole(data.roleText.value)" align="center"></UserDataSlot>
						<UserStatusSlot :status="data.verificationStatus" align="center"></UserStatusSlot>
						<UserDataSlot :text="dateLocale(data.createdAt)" align="center"></UserDataSlot>
						<UserDataSlot :text="datetime(data.latestLoginAt)" align="center"></UserDataSlot>

						<UserActionSlot :id="data._id" :status="data.verificationStatus" @reload="$emit('reload')"></UserActionSlot>
					</tr>
				</template>
			</tbody>
		</table>
		<div v-if="tData.length == 0" tabindex="0" colspan="9" class="text-xs h-16 bg-white rounded hover:bg-theme-green-100 align-middle cursor-pointer">
			<div class="flex justify-center items-center">
				<span class="font-medium text-xs text-theme-black-300 mt-5">{{ $t("alert.no_data") }}</span>
			</div>
		</div>
	</div>
</template>

<script>
import moment from "moment";
export default {
	props: {
		tHead: {
			type: Array,
			require: true,
		},
		tData: {
			type: Array,
			require: true,
		},
	},
	data() {
		return {};
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
		async setSort(key, value, index) {
			await this.tHead.map((item, idx) => {
				if (idx !== index) {
					item.sortValue = 0;
				}
				// console.log(item.sortValue);
				return item;
			});
			this.$emit("sort", { key: key, value: value });
		},
		userRole(role) {
			switch (role) {
				case 0:
					return this.$t("user.role.user");
				case 1:
					return this.$t("user.role.registrar");
				case 99:
					return this.$t("user.role.admin");
				default:
					return "N/A";
			}
		},
		dateToString(data) {
			return moment(data).format("YYYY-MM-DD");
		},
		dateLocale(date) {
			if (!date) {
				return "-";
			}
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY");
			// return this.$dayjs(date).locale("en").format("DD MMM YYYY");
		},
		datetime(date) {
			if (!date) {
				return "-";
			}
			if (this.$i18n.locale === "th") {
				return this.$dayjs(date).locale("th").format("DD MMM BBBB (HH:mm)");
			}
			return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
			// return this.$dayjs(date).locale("en").format("DD MMM YYYY (HH:mm)");
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
			this.$router.push(this.localePath("/project/" + id));
		},
		deleteUser(id) {
			const app = this;
			this.$swal
				.fire({
					icon: "info",
					iconColor: "#ef4444",
					title: this.$t("alert.title.warning"),
					text: this.$t("alert.text.warning.delete"),
					showCancelButton: true,

					confirmButtonColor: "#ef4444",
					confirmButtonText: this.$t("button.confirm"),
					cancelButtonText: this.$t("button.cancel"),
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.$axios
							.$delete(`/api/v1/user/${app.$route.params.id}`)
							.then((resp) => {
								// console.log(resp);
								app.$router.push(app.localePath({ name: "users" }));
								// app.form = resp;
								app.$swal.fire({
									icon: "success",
									iconColor: "#059669",
									confirmButtonColor: "#059669",
									title: this.$t("alert.title.success.delete"),
									timer: 2000,
									timerProgressBar: true,
								});
							})
							.catch((err) => {
								app.$swal.fire({
									icon: "error",
									title: this.$t("alert.title.error.delete"),
								});
								console.log(err);
							});
					}
				});
		},
	},
};
</script>
