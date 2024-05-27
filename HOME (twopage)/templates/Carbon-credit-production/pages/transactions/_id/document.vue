<template>
	<div class="w-full h-full">
		<PDFModal v-if="pdfModal" @close="closeTab" :pdfURL="pdfURL"></PDFModal>
	</div>
</template>

<script>
export default {
	name: "DocumentPage",
	layout: "MainLayout",
	data() {
		return {
			pdfModal: false,
			pdfURL: "",
			document: {
				th: [],
				en: [],
			},
		};
	},
	mounted() {
        this.pdfURL = `${process.env.baseUrl}/api/v1/transaction/download/${this.$route.params.id}`;
        this.pdfModal = true;
	},
	methods: {
        closeTab() {
            window.close();
        },
		showPDF(url) {
			this.pdfModal = true;
			this.pdfURL = process.env.baseUrl + url;
			// this.$swal('test')
			// window.open(url, '_blank');
		},
	},
};
</script>

<style>
</style>