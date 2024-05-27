<template>
	<div class="w-full pt-4">
		<div class="grid grid-cols-4 gap-4">
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.account_type.title')" :required="true" />
				<UIDropdown v-model.number="form.account_type" :option="dropdowns.account_types" />
				<UIErrorMsg v-if="!$v.form.account_type.required && isSubmitted">{{ $t("openAccount.validate.account_type") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('user.table.header.role')" :required="true" />
				<UIDropdown v-model.number="form.role" :option="dropdowns.roles" />
				<UIErrorMsg v-if="!$v.form.role.required && isSubmitted">{{ $t("openAccount.validate.role") }}</UIErrorMsg>
			</div>
			<div class="col-span-4">
				<UILabel :text="$t('openAccount.organization')" :required="true" />
				<UIDropdown v-model.number="form.companyID" :option="dropdowns.organization" :labelAttr="$i18n.locale" />
				<UIErrorMsg v-if="!$v.form.companyID.required && isSubmitted">{{ $t("openAccount.validate.organization") }}</UIErrorMsg>
			</div>
			<div class="col-span-4 grid grid-cols-4 gap-4 bg-gray-50 rounded-md p-2 border" v-if="selectedOrganization.value">
				<div class="col-span-2">
					<UILabel :text="$t('openAccount.form.phone_number')" />
					<p>{{ selectedOrganization.data.phone }}</p>
				</div>
				<div class="col-span-2">
					<UILabel :text="$t('openAccount.form.government.address')" />
					<p>{{ selectedOrganization.data.address }}</p>
				</div>

				<div class="col-span-1">
					<UILabel :text="$t('openAccount.form.province')" />
					<p>{{ selectedOrganization.data.province }}</p>
				</div>
				<div class="col-span-1">
					<UILabel :text="$t('openAccount.form.district')" />
					<p>{{ selectedOrganization.data.district }}</p>
				</div>
				<div class="col-span-1">
					<UILabel :text="$t('openAccount.form.subdistrict')" />
					<p>{{ selectedOrganization.data.subdistrict }}</p>
				</div>
				<div class="col-span-1">
					<UILabel :text="$t('openAccount.form.postcode')" />
					<p>{{ selectedOrganization.data.postcode }}</p>
				</div>

				<div class="col-span-4">
					<table class="border w-full">
						<tr class="border divide-x h-20 text-sm">
							<td class="w-1/12 text-center p-2 bg-gray-100">1.</td>
							<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.verified1") }}</td>
							<td class="w-5/12 p-2 text-center">
								<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(selectedOrganization.data?.document.verified.src)">{{ selectedOrganization.data?.document.verified.name }}</span>
							</td>
						</tr>
						<tr class="border divide-x h-20 text-sm">
							<td class="w-1/12 text-center p-2 bg-gray-100">2.</td>
							<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.authorize") }}</td>
							<td class="w-5/12 p-2 text-center">
								<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(selectedOrganization.data?.document.authorize.src)">{{ selectedOrganization.data?.document.authorize.name }}</span>
							</td>
						</tr>
						<tr class="border divide-x h-20 text-sm">
							<td class="w-1/12 text-center p-2 bg-gray-100">3.</td>
							<td class="w-5/12 p-2 bg-gray-50">{{ $t("openAccount.showDocument.card_id_representative") }}</td>
							<td class="w-5/12 p-2 text-center">
								<span class="truncate hover:underline cursor-pointer" :title="$t('button.see')" @click="openPDF(selectedOrganization.data?.document.card_id_representative.src)">{{ selectedOrganization.data?.document.card_id_representative.name }}</span>
							</td>
						</tr>
					</table>
					<PDFModal v-if="pdfModal" @close="pdfModal = false" :pdfURL="pdfURL" />
					<client-only placeholder="loading...">
						<EasyLightBox :imgs="imgSrc" :visible="visible" :index="index" @hide="visible = false"> </EasyLightBox>
					</client-only>
				</div>
				<div class="col-span-4 flex justify-end">
					<a class="text-blue-500 hover:underline text-sm flex items-center gap-1" target="__blank" :href="`/organization/${selectedOrganization.data._id}/edit`">
						{{ $t("button.edit") }}
						<font-awesome-icon icon="fa-solid fa-pen" />
					</a>
				</div>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.email')" :required="true" />
				<UITextInput v-model="form.email" />
				<UIErrorMsg v-if="!$v.form.email.required && isSubmitted">{{ $t("openAccount.validate.email") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.email.email && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
			</div>
			<div class="col-span-2 space-y-3">
				<UILabel :text="$t('openAccount.form.request_permission.title')" :required="true" />
				<AuthRequestPermission :form="form" />
				<UIErrorMsg v-if="!$v.form.request_permission.morethan1 && isSubmitted">{{ $t("openAccount.validate.requestPermission") }}</UIErrorMsg>
			</div>

			<div class="col-span-4"></div>
			<div class="col-span-4 border-t"></div>
			<div class="col-span-4"></div>

			<div class="col-span-4">
				<p class="text-base underline">{{ $t("openAccount.form.juristic.grantee_info.title") }}</p>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.firstname')" :required="true" />
				<UITextInput v-model="form.firstname" />
				<UIErrorMsg v-if="!$v.form.firstname.required && isSubmitted">{{ $t("openAccount.validate.firstname") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.firstname.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.firstname.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-1">
				<UILabel :text="$t('openAccount.form.lastname')" :required="true" />
				<UITextInput v-model="form.lastname" />
				<UIErrorMsg v-if="!$v.form.lastname.required && isSubmitted">{{ $t("openAccount.validate.lastname") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.lastname.containsNotSpecial && isSubmitted">{{ $t("openAccount.validate.containsNotSpecial") }}</UIErrorMsg>
				<UIErrorMsg v-if="!$v.form.lastname.minLength && isSubmitted">{{ $t("openAccount.validate.minLength2") }}</UIErrorMsg>
			</div>
			<div class="col-span-2">
				<UILabel :text="$t('openAccount.form.card_id')" :required="true" />
				<UITextInput v-model="form.card_id" />
				<UIErrorMsg v-if="!$v.form.card_id.required && isSubmitted">{{ $t("openAccount.validate.id_card") }}</UIErrorMsg>
			</div>

			<div class="col-span-4"></div>
		</div>
	</div>
</template>

<script>
	import EasyLightBox from "vue-easy-lightbox";
	import { required, sameAs, minLength, email } from "vuelidate/lib/validators";
	import UploadImage from "../../static/mixins/upload-image";
	export default {
		props: ["form", "isSubmitted"],
		mixins: [UploadImage],
		components: {
			EasyLightBox,
		},
		data() {
			return {
				dropzoneOptions: {
					url: process.env.baseUrl + "/api/v1/form/upload",
					disablePreviews: true,
					previewsContainer: false,
					parallelUploads: 10,
					maxFiles: 10,
					acceptedFiles: "image/png,image/jpeg,application/pdf",
				},
				dropdowns: {
					roles: [
						{ value: 0, text: this.$t("user.role.user") },
						{ value: 1, text: this.$t("user.role.registrar") },
						{ value: 99, text: this.$t("user.role.admin") },
					],
					provinces: [],
					district: [],
					subdistrict: [],
					organization: [],
					account_types: [
						{ text: this.$t("openAccount.account_type.option.guest"), value: 0 },
						{ text: this.$t("openAccount.account_type.option.juristic"), value: 1 },
						{ text: this.$t("openAccount.account_type.option.government"), value: 2 },
					],
				},
				idOption: "idcard",
				// isSubmitted: false,
				pdfModal: false,
				visible: false,
				index: 0,
				imgSrc:''
			};
		},
		computed: {
			selectedOrganization() {
				const com = this.dropdowns.organization.find((e) => e.value === this.form.companyID);
				if (com) return com;
				return {
					value: null,
					th: "-",
					en: "-",
					data: {
						_id: null,
						phone: null,
						address: null,
						province: null,
						district: null,
						subdistrict: null,
						postcode: null,
						document: {
							verified: {
								name: null,
								src: null,
							},
							authorize: {
								name: null,
								src: null,
							},
							card_id_representative: {
								name: null,
								src: null,
							},
						},
					},
				};
			},
		},
		validations() {
			return {
				form: {
					account_type: { required },
					role: { required },
					// accountName: { required, minLength: minLength(2) },
					firstname: { required, containsNotSpecial: (value) => !/[#?!@$%^&*/]/.test(value), minLength: minLength(2) },
					lastname: { required, containsNotSpecial: (value) => !/[#?!@$%^&*/]/.test(value), minLength: minLength(2) },
					companyID: { required },

					email: {
						required,
						email,
					},
					request_permission: {
						morethan1: () => this.form.request_permission.length > 0,
					},
					card_id: { required },
				},
			};
		},

		async mounted() {
			if(this.form.company) {
				if(this.form.company.companyType === 1) {
					this.form.companyID = null;
				}else if(this.form.company.companyType === 2) {
					this.form.companyID = this.form.company.companyId;
				}
			}else{
				this.form.companyID = null;
			}
			await this.getOrganization();
			await this.getProvince();
			await this.getDistrict();
			await this.getSubdistrict();
		},
		methods: {
			async getOrganization() {
				const app = this;
				this.dropdowns.organization = await this.$axios
					.$get(`/api/v1/dropdown/organization?companyType=2`)
					.then((resp) => resp)
					.catch((err) => {
						console.log(err);
					});
			},
			openPDF(src) {
				this.pdfURL = process.env.baseUrl + src;
				this.imgSrc = process.env.baseUrl + src;
				if (/(.png|.jpg|.jpeg)/.test(src)) {
					this.visible = true;
				} else {
					this.pdfModal = true;
				}
			},
			next_step() {
				this.isSubmitted = true;
				this.$v.$touch();
				if (this.$v.$invalid) {
					this.$swal.fire({
						icon: "error",
						iconColor: "#ef4444",
						confirmButtonColor: "#ef4444",
						title: this.$t("sweetalert.complete_information"),
						text: this.$t("sweetalert.complete_information_text"),
					});

					return 0;
				}
				this.$emit("click");
			},
			async getProvince() {
				const app = this;
				this.dropdowns.provinces = await this.$axios
					.$get(`/api/v1/dropdown/provinces`)
					.then((resp) => resp)
					.catch((err) => {
						console.log(err);
					});
			},
			async getDistrict() {
				const app = this;
				// console.log("province");

				this.dropdowns.district = await this.$axios
					.$get(`/api/v1/dropdown/district?province=${this.form.province}`)
					.then((resp) => resp)
					.catch((err) => {
						console.log(err);
					});
			},
			async getSubdistrict() {
				const app = this;

				this.dropdowns.subdistrict = await this.$axios
					.$get(`/api/v1/dropdown/subdistrict?province=${this.form.province}&district=${this.form.district}`)
					.then((resp) => resp)
					.catch((err) => {
						console.log(err);
					});
			},

			validateForm() {
				// this.isSubmitted = true;
				this.$v.$touch();
				return this.$v.$invalid;
			},

			async uploadImage(input, key) {
				if (input.target.files[0]) {
					const formData = new FormData();
					const fileItem = input.target.files[0];
					// console.log(fileItem);
					formData.append("file", fileItem);
					const resp = await this.uploadImages(formData);
					// console.log(resp);
					this.form.company.document[key] = resp;
				}
			},
		},
	};
</script>

<style></style>
