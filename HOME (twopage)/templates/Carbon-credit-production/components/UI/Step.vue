<template>
	<div class="w-full">
		<div class="grid grid-cols-5 text-sm border border-gray-300 rounded divide-x divide-gray-300 bg-white">
			<div class="col-span-1 flex items-center relative">
				<div class="px-2 md:px-4 py-2 w-full" :class="{ 'border-b-4 border-tgo-teal-500': step == 1 }">
					<div class="flex items-center gap-2">
						<div :class="`w-10 h-10 rounded-full border-2 border-gray-300 hidden md:flex items-center justify-center ${highlightStep1}`">
							<p v-if="!done1">01</p>
							<div v-else>
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
									<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
								</svg>
							</div>
						</div>
						<div class="text-xs md:text-md" :class="{ 'text-tgo-teal-500': step >= 1 }">{{ $t("openAccount.stepbar.step1") }}</div>
					</div>
				</div>
			</div>
			<div class="col-span-1 flex items-center">
				<div class="px-2 md:px-4 py-2 w-full" :class="{ 'border-b-4 border-tgo-teal-500': step == 2 }">
					<div class="flex items-center gap-2">
						<div :class="`w-10 h-10 rounded-full border-2 border-gray-300 hidden md:flex items-center justify-center ${highlightStep2}`">
							<p v-if="!done2">02</p>
							<div v-else>
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
									<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
								</svg>
							</div>
						</div>
						<div class="text-xs md:text-md"  :class="{ 'text-tgo-teal-500': step >= 2 }">{{ $t("openAccount.stepbar.step2") }}</div>
					</div>
				</div>
			</div>
			<div class="col-span-1 flex items-center">
				<div class="px-2 md:px-4 py-2 w-full" :class="{ 'border-b-4 border-tgo-teal-500': step == 3 }">
					<div class="flex items-center gap-2">
						<div :class="`w-10 h-10 rounded-full border-2 border-gray-300 hidden md:flex items-center justify-center ${highlightStep3}`">
							<p v-if="!done3">03</p>
							<div v-else>
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
									<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
								</svg>
							</div>
						</div>
						<div class="text-xs md:text-md"  :class="{ 'text-tgo-teal-500': step >= 3 }">{{ $t("openAccount.stepbar.step3") }}</div>
					</div>
				</div>
			</div>
			<div class="col-span-1 flex items-center">
				<div class="px-2 md:px-4 py-2 w-full" :class="{ 'border-b-4 border-tgo-teal-500': step == 4 }">
					<div class="flex items-center gap-2">
						<div :class="`w-10 h-10 rounded-full border-2 border-gray-300 hidden md:flex items-center justify-center ${highlightStep4}`">
							<p v-if="!done4">04</p>
							<div v-else>
								<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
									<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
								</svg>
							</div>
						</div>
						<div class="text-xs md:text-md"  :class="{ 'text-tgo-teal-500': step >= 4 }">{{ $t("openAccount.stepbar.step4") }}</div>
					</div>
				</div>
			</div>
			<div class="col-span-1">
				<div class="px-2 md:px-4 py-2" :class="{ 'border-b-4 border-tgo-teal-500': step == 5 }">
					<div class="flex items-center gap-2">
						<div :class="`w-10 h-10 rounded-full border-2 border-gray-300 hidden md:flex items-center justify-center ${highlightStep4}`">
							<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
							</svg>
						</div>
						<div class="text-xs md:text-md"  :class="{ 'text-tgo-teal-500': step == 5 }">{{ $t("openAccount.stepbar.step5") }}</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: ["step"],
	data() {
		return {
			done1: false,
			done2: false,
			done3: false,
			done4: false,
		};
	},
	computed: {
		highlightStep1() {
			if (this.step === 1) {
				return "text-tgo-teal-500 border-tgo-teal-500";
			} else if (this.step > 1) {
				return "text-white border-tgo-teal-500 bg-tgo-teal-500";
			}
			return "";
		},
		highlightStep2() {
			if (this.step === 2) {
				return "text-tgo-teal-500 border-tgo-teal-500";
			} else if (this.step > 2) {
				return "text-white border-tgo-teal-500 bg-tgo-teal-500";
			}
			return "";
		},
		highlightStep3() {
			if (this.step === 3) {
				return "text-tgo-teal-500 border-tgo-teal-500";
			} else if (this.step > 3) {
				return "text-white border-tgo-teal-500 bg-tgo-teal-500";
			}
			return "";
		},
		highlightStep4() {
			if (this.step === 4) {
				return "text-tgo-teal-500 border-tgo-teal-500";
			} else if (this.step > 4) {
				return "text-white border-tgo-teal-500 bg-tgo-teal-500";
			}
			return "";
		},
	},
	watch: {
		step(val) {
			if (val === 1) {
				this.done1 = false;
				this.done2 = false;
				this.done3 = false;
				this.done4 = false;
			}
			if (val > 1) {
				this.done1 = true;
				this.done2 = false;
				this.done3 = false;
				this.done4 = false;
			}
			if (val > 2) {
				this.done2 = true;

				this.done3 = false;
				this.done4 = false;
			}
			if (val > 3) {
				this.done3 = true;

				this.done4 = false;
			}
			if (val > 4) {
				this.done4 = true;
			}
		},
	},
};
</script>

<style>
</style>