<template>
	<div class="w-full pt-4">
		<div class="pb-4">
			<p class="text-green-600 sm:text-lg md:text-xl">{{ $t("openAccount.agreement.title") }}</p>
		</div>
		<div class="bg-gray-50 h-full overflow-y-auto p-4 text-sm space-y-4 whitespace-normal w-full font-thin">
			<div>
				<p class="break-words indent-16 sm:text-md md:text-lg">{{ $t("openAccount.agreement.sentense") }}</p>
			</div>
			<div>
				<p class="indent-16 sm:text-md md:text-lg">{{ $t("openAccount.agreement.sentense1") }}</p>
			</div>
			<div id="consents1">
				<p class="indent-16 sm:text-md md:text-lg">{{ $t("openAccount.agreement.p1") }}</p>

				<div class="flex items-center justify-center py-10">
					<div class="flex gap-10 items-center justify-center">
						<label class="flex gap-2">
							<input disabled v-model="form.consents.for_notification" type="radio" :value="true" name="permission1" class="w-5 h-5 bg-white" />
							{{$t('button.accept')}}
						</label>

						<label class="flex gap-2">
							<input disabled v-model="form.consents.for_notification" type="radio" :value="false" name="permission1" class="w-5 h-5 bg-white" />
							{{$t('button.unaccept')}}
						</label>
					</div>
				</div>
			</div>
			<div id="consents2">
				<p class="indent-16 sm:text-md md:text-lg">{{ $t("openAccount.agreement.p2") }}</p>

				<div class="flex items-center justify-center py-10">
					<div class="flex gap-10 items-center justify-center">
						<label class="flex gap-2">
							<input disabled v-model="form.consents.for_public_nonsensitive_information" type="radio" :value="true" name="permission2" class="w-5 h-5 bg-white" />
							{{$t('button.accept')}}
						</label>

						<label class="flex gap-2">
							<input disabled v-model="form.consents.for_public_nonsensitive_information" type="radio" :value="false" name="permission2" class="w-5 h-5 bg-white" />
							{{$t('button.unaccept')}}
						</label>
					</div>
				</div>
			</div>

			<div id="consents3">
				<p class="indent-16 sm:text-md md:text-lg">{{ $t("openAccount.agreement.p3") }}</p>

				<div class="flex items-center justify-center py-10">
					<div class="flex gap-10 items-center justify-center">
						<label class="flex gap-2">
							<input disabled v-model="form.consents.for_development" type="radio" :value="true" name="permission3" class="w-5 h-5 bg-white" />
							{{$t('button.accept')}}
						</label>

						<label class="flex gap-2">
							<input disabled v-model="form.consents.for_development" type="radio" :value="false" name="permission3" class="w-5 h-5 bg-white" />
							{{$t('button.unaccept')}}
						</label>
					</div>
				</div>
			</div>
			<div id="consents4">
				<p class="text-justify indent-16 pt-2 sm:text-md md:text-lg">{{ $t("openAccount.agreement.p4_1") }}</p>
				<p class="text-justify indent-16 pt-2 sm:text-md md:text-lg">{{ $t("openAccount.agreement.p4_2") }}</p>
				<p class="text-justify indent-16 pt-2 sm:text-md md:text-lg">{{ $t("openAccount.agreement.p4_3") }}</p>
				<p class="text-justify indent-16 pt-2 sm:text-md md:text-lg">{{ $t("openAccount.agreement.p4_4") }}</p>

			</div>
		</div>
		
	</div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
export default {
	props: ["form"],
	methods: {
		next_step() {
			this.$v.$touch();
			if (this.$v.$invalid) {
				this.$swal.fire({
					icon: "error",
					iconColor: "#ef4444",
					confirmButtonColor: "#ef4444",
					title: this.$t("sweetalert.invalid"),
					text: this.$t("กรุณาระบุคำยินยอม"),
				});
				return 0;
			}
			this.$emit("click");
		},
	},
	validations() {
		return {
			form: {
				consents: {
					for_notification: { required },
					for_public_nonsensitive_information: { required },
					for_development: { required },
				},
			},
		};
	},
};
</script>

<style>
.indent-16 {
	text-indent: 4rem;
}
</style>