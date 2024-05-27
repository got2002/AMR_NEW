<template>
	<div class="w-full h-full">
		<div class="w-full mb-5">
			<p class="text-xl font-bold">{{ $t("document.page_title") }}</p>
		</div>
		<div class="w-full bg-white p-4 shadow-sm rounded">
			<dl class="space-y-2">
				<dt class="font-semibold text-base">{{ $t("document.th") }}</dt>
				<dd v-for="doc in document.th" :key="doc._id" @click="showPDF(doc.url)" class="text-sm hover:underline hover:text-tgo-teal-500 transform ease-out duration-100 cursor-pointer ml-4">> {{ doc.name }}</dd>

				<dt class="font-semibold text-base">{{ $t("document.en") }}</dt>
				<dd v-for="doc in document.en" :key="doc._id" @click="showPDF(doc.url)" class="text-sm hover:underline hover:text-tgo-teal-500 transform ease-out duration-100 cursor-pointer ml-4">> {{ doc.name }}</dd>
			</dl>
		</div>
		<PDFModal v-if="pdfModal" @close="pdfModal = false" :pdfURL="pdfURL"></PDFModal>
	</div>
</template>

<script>
export default {
	name: "DocumentPage",
	layout: "MainLayout",
	data() {
		return {
			edit: false,
			pdfModal: false,
			pdfURL: "",
			document: {
				th: [],
				en: [],
			},
		};
	},
	mounted() {
		this.getDocument();
	},
	methods: {
		showPDF(url) {
			this.pdfModal = true;
			this.pdfURL = process.env.baseUrl + url;
			// this.$swal('test')
			// window.open(url, '_blank');
		},
		getDocument() {
			const app = this;
			this.$axios.$get("/api/v1/documents").then((resp) => {
				app.document.th = resp.th;
				app.document.en = resp.en;
			});
		},
	},
};
</script>

<style>
</style>