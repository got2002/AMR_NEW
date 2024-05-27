<template>
	<section class="pt-2 pb-4">
		<div class="flex justify-between items-center mb-10">
			<h2 class="text-3xl font-bold">{{ $t("project.view_page.page_title") }} # {{ data.project_id }}</h2>
			<div class="flex gap-2">
				<!-- <nuxt-link :to="localePath('/')" class="px-6 py-3 text-center bg-gray-500 rounded shadow-sm text-white hover:bg-gray-600">{{ $t("button.back") }}</nuxt-link> -->
				<UIBackButton @click="$router.push(localePath('/'))" padding="py-3 px-4">{{ $t("button.back") }}</UIBackButton>
			</div>
		</div>
		<ProjectSkeletonLoad v-if="loading"></ProjectSkeletonLoad>
		<div v-if="!loading" class="flex items-start gap-4">
			<div id="info" class="flex flex-col w-1/2 bg-white shadow-md p-4">
				<h2 v-if="$i18n.locale === 'th'" class="mb-1 text-lg font-bold">{{ data.project_name?.thai }}</h2>
				<h2 v-if="$i18n.locale === 'th'" class="mb-1 text-sm font-bold text-gray-500">{{ data.project_name?.english }}</h2>
				<h2 v-if="$i18n.locale === 'en'" class="mb-1 text-lg font-bold">{{ data.project_name?.english }}</h2>
				<h2 v-if="$i18n.locale === 'en'" class="mb-1 text-sm font-bold text-gray-500">{{ data.project_name?.thai }}</h2>
				<div class="col-span-1 bg-theme-black-50 bg-opacity-50 p-4 gap-3 mt-5">
					<div class="flex">
						<div class="text-sm font-bold">{{ $t("project.view_page.knp_rule") }} :</div>
						<div class="px-2 text-sm break-words">
							{{ ccmgm(data.project_type_by_extens) }}
						</div>
					</div>

					<div class="flex">
						<div class="text-sm font-bold">{{ $t("project.view_page.standard") }} :</div>
						<div class="px-2 text-sm break-words">
							{{ data.standard || $t("undefined") }}
						</div>
					</div>
					<div class="flex">
						<div class="text-sm font-bold">{{ $t("project.view_page.programid") }} :</div>
						<div class="px-2 text-sm">
							{{ data.programID || $t("undefined") }}
						</div>
					</div>
					<div class="flex">
						<div class="text-sm font-bold">{{ $t("project.view_page.authorizeduse") }} :</div>
						<div class="px-2 text-sm">
							{{ dropdowns.authorizedUse.find((auth) => auth.value === data.authorizedUse)?.text || $t("undefined") }}
						</div>
					</div>
					<div class="flex">
						<div class="text-sm font-bold">{{ $t("project.view_page.reference_link") }} :</div>
						<div class="px-2 text-sm">
							<a :href="data?.reference_link" target="_blank" class="hover:underline hover:text-blue-500 cursor-pointer">{{ data?.reference_link || $t("undefined") }}</a>
						</div>
					</div>
				</div>
				<div class="bg-theme-black-50 bg-opacity-50 p-4 gap-3 mt-5">
					<div class="text-sm font-bold">{{ $t("project.view_page.project_overview") }}</div>
					<div class="text-sm break-words">{{ projectActivityLang(data.project_activity) }}</div>
				</div>
				<div class="mt-5">
					<label class="text-sm font-bold">{{ $t("project.view_page.co_benefit") }}</label>
					<ProjectCoBenefit :form="data" />
				</div>

				<ProjectGeneralInfo :data="data"></ProjectGeneralInfo>

				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="">
					{{ $t("project.create_page.reduction_methods.title") }}
					<ProjectReductionMethod :form="data" />
				</div>

				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div class="">
					{{ $t("project.view_page.registered_doc") }}
					<ProjectTablePDF :form="data" />
				</div>
				<div class="h-1 border-t-2 border-dashed my-5"></div>
				<div class="">
					{{ $t("project.view_page.additional_doc") }}
					<ProjectShowAdditionalDocument :form="data" />
				</div>
			</div>
			<div class="flex flex-col w-1/2 pl-4 bg-white shadow-md p-4">
				<div class="grid grid-cols-1 gap-2">
					<div class="flex items-center justify-between">
						<div>{{ $t("project.view_page.project_status") }}</div>
						<div
							class="px-3 py-3 rounded text-base border"
							:class="{
								'bg-red-500 bg-opacity-10 text-red-500 border-red-500': data.status == 'Cancelled',
								'bg-green-500 bg-opacity-10 text-green-500 border-green-500': data.status == 'Registered',
								'bg-gray-500 bg-opacity-10 text-gray-500 border-gray-500': data.status == 'Expired',
							}"
						>
							{{ statusLang(data.status) }}
						</div>
					</div>
				</div>
				<div class="h-1 border-t-2 border-dashed my-5"></div>

				<div v-if="edit_approval.value == 1" class="flex flex-col justify-center items-center w-full col-span-2 mb-5">
					<label for="dropzone-file" class="flex flex-col z-0 justify-center items-center w-3/4 h-64 bg-gray-50 rounded-lg border-2 border-gray-300 border-dashed cursor-pointer dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
						<div class="flex flex-col justify-center items-center pt-5 pb-6" v-if="fileArr.length == 0">
							<svg class="mb-3 w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
							<p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
								<span class="font-semibold">{{ $t("project.view_page.Click_to_select_a_file") }}</span> {{ $t("project.view_page.or_drag") }}
							</p>
							<p class="text-xs text-gray-500 dark:text-gray-400">SVG, PNG, JPG, PDF or GIF</p>
						</div>
						<div class="w-full grid grid-cols-4 gap-2 items-center justify-center p-5" v-if="fileArr.length > 0">
							<div class="col-span-1 bg-white shadow-sm border rounded-md relative" v-for="(img, idx) in fileArr" :key="idx">
								<div @click="removeImg(idx)" class="absolute z-50 -right-3 -top-3 p-2 rounded-full bg-gray-200 border shadow-sm">
									<font-awesome-icon icon="fas fa-times"></font-awesome-icon>
								</div>
								<img :src="img" class="w-full rounded-md" />
							</div>
						</div>
						<input id="dropzone-file" type="file" accept="image/png, image/gif, image/jpeg, image/svg, application/pdf" class="hidden" @change="uploadImages" multiple />
					</label>
					<div class="flex w-full justify-center items-center mt-5">
						<div class="text-sm font-bold mr-2">{{ $t("project.view_page.amount") }}:</div>
						<input type="number" v-model.number="form.amount" class="form-control block w-1/4 px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-tgo-yellow-500 focus:outline-none" />
					</div>
				</div>
				<div v-if="edit_approval.value == 2" class="flex flex-col justify-center items-center w-full col-span-2 mb-5">
					<div class="flex justify-center">
						<div class="xl:w-96">
							<label for="exampleFormControlTextarea1" class="form-label inline-block mb-2 text-gray-700">{{ $t("project.view_page.message_to_user") }}</label>
							<textarea v-model="form.message" class="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-tgo-yellow-500 focus:outline-none" rows="3"></textarea>
						</div>
					</div>
				</div>
				<div v-if="edit_approval.value != 0" class="flex items-center justify-center gap-4 mb-5">
					<button @click="updateProject()" class="w-20 py-2 border border-tgo-teal-500 text-white bg-tgo-teal-500 hover:bg-theme-green-200 hover:text-theme-white">{{ $t("button.save") }}</button>
				</div>

				<div class="text-sm font-bold mb-2">{{ $t("project.create_page.project_images") }}</div>
				<ProjectImage :form="data" :editMode="false"></ProjectImage>

				<div class="h-1 border-t-2 border-dashed my-5"></div>
				<ProjectMapInfo v-if="data.location?.features.length != 0" :form="data" :height="18" :heightUnit="'rem'" class="flex-grow w-full" />
				<div class="bg-theme-black-50 bg-opacity-50 p-4 flex gap-3 mt-3 justify-between">
					<div v-html="$t('project.view_page.estimated_greenhouse_gases_reduction')" class="text-sm font-bold"></div>

					<div class="text-base font-bold mr-3">
						{{ data.approx_co2_reduction_per_year.toLocaleString() }}
					</div>
				</div>

				<div class="mt-3">
					{{ $t("project.view_page.carbon_credits_verified_table") }}
					<ProjectTableCarbon2 :form="data" :edit="false" />
				</div>
				<div class="bg-theme-black-50 p-4 bg-opacity-50 flex gap-3 justify-between rounded mt-3 border">
					<div v-html="$t('project.view_page.approved_carbon_credits')" class="text-sm font-bold"></div>
					<div class="text-base font-bold mr-3">
						{{ sumCarbon(data.carbon_credit_cert) }}
					</div>
				</div>
			</div>
			<!-- <loadingCarbon v-if="!isData" /> -->
		</div>
	</section>
</template>

<script>
import dropdowns from "../../../mixins/dropdowns";
export default {
	name: "ProjectPreview",
	layout: "MainLayout",
	mixins: [dropdowns],
	// middleware: ["auth"],

	asyncData({ params }) {
		const id = params.id;
		return { id };
	},
	data() {
		return {
			data: {},
			isData: false,
			edit_approval: {
				text: null,
				value: 0,
			},
			fileArr: [],
			form: {
				status: null,
				amount: 0,
				certified_files: [],
				message: "",
			},
			dropdowns: {
				authorizedUse: [],
			},
			loading: true,
		};
	},
	async mounted() {
		this.dropdowns.authorizedUse = await this.getDropdownAutherizedUse();
		this.getProject();
	},
	methods: {
		statusLang(data) {
			if (this.$i18n.locale === "en") {
				return data;
			} else {
				switch (data) {
					case "Registered":
						return "ขึ้นทะเบียนแล้ว";
					case "Cancelled":
						return "ยกเลิกโครงการ";
					case "Expired":
						return "สิ้นสุดโครงการ";
					default:
						return "ขึ้นทะเบียนแล้ว";
				}
			}
		},
		projectActivityLang() {
			if (this.$i18n.locale === "th") {
				return this.data.project_activity;
			}
			return this.data.project_activity_en;
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

		updateProject() {
			const app = this;
			this.$swal
				.fire({
					icon: "info",
					iconColor: "#f59e0b",
					title: this.$t("sweetalert.confirm_correction"),
					text: this.$t("sweetalert.Please_confirm_the_correction"),
					showCancelButton: true,
					reverseButtons: true,

					confirmButtonColor: "#f59e0b",
					confirmButtonText: this.$t("sweetalert.confirm"),
					cancelButtonText: this.$t("sweetalert.cancel"),
				})
				.then((result) => {
					if (result.isConfirmed) {
						app.$axios
							.$post(`/api/v1/project/approval/${app.$route.params.id}`, app.form)
							.then((resp) => {
								// console.log(resp);
								app.getProject();
								// app.form = resp;
								app.$nuxt.refresh();
								app.$swal.fire({
									icon: "success",
									iconColor: "#059669",
									confirmButtonColor: "#059669",
									title: app.$t("sweetalert.Correction_succeeded"),
									timer: 2000,
									timerProgressBar: true,
								});
							})
							.catch((err) => {
								console.log(err);
							});
					}
				});
		},
		async uploadImages(input) {
			const app = this;
			const fileLength = input.target.files.length;
			for (let i = 0; i < fileLength; i++) {
				const formData = new FormData();
				const fileItem = input.target.files[i];
				// console.log(fileItem);
				formData.append("file", fileItem);
				await this.$axios
					.$post(`/api/v1/form/upload`, formData)
					.then((resp) => {
						app.form.certified_files.push(resp);
						// console.log(app.form.certified_files);
					})
					.catch((err) => {
						console.log(err);
					});
				const reader = new FileReader();
				reader.onload = function (e) {
					app.fileArr.push(e.target.result);
				};

				reader.readAsDataURL(fileItem);
			}
		},
		removeImg(idx) {
			this.fileArr.splice(idx, 1);
			this.form.certified_files.splice(idx, 1);
		},
		verification(value) {
			if (this.edit_approval.value === 1 && value === 1) {
				this.edit_approval.value = 0;
				this.form.status = null;
			} else if (this.edit_approval.value === 2 && value === 2) {
				this.edit_approval.value = 0;
				this.form.status = null;
			} else {
				if (value === 1) {
					this.form.status = "Verified";
				} else {
					this.form.status = "Rejected";
				}
			}
		},
		async getProject() {
			const app = this;
			app.loading = true;
			await this.$axios
				.$get(`/api/v1/home/${this.id}`)
				.then((resp) => {
					// console.log(resp);
					app.data = resp;
					app.isData = true;
					app.loading = false;
					app.data.carbon_credit_cert.sort(function (a, b) {
						return new Date(a.end_date) - new Date(b.end_date);
					});
					// this.$toast.success("เพิ่มข้อมูลสำเร็จ");
					// this.$router.push("/users/userManagement");
					// setTimeout(this.$toast.clear, 3000);
				})
				.catch((errors) => {
					console.log(errors);
					app.loading = false;

					// this.$toast.error(errors.response.data.errors);
					// setTimeout(this.$toast.clear, 3000);
					app.isData = true;
				});
		},
		dateToString(date) {
			const result = new Date(date).toLocaleDateString("th-TH", {
				year: "numeric",
				month: "long",
				day: "numeric",
			});
			return result;
		},
		sumCarbon(data) {
			let sum = 0;
			const app = this;
			data.forEach((element) => {
				sum += app._.sumBy(element.data, (item) => item.amount);
			});
			return sum.toLocaleString();
		},
	},
};
</script>

<style></style>
