export default {
    data() {
        return {
            thaiformatter: {
                stringify: (date) => {
                    if (!date) return "";
                    else {
                        if (this.$i18n.locale === "th") {
                            const dm = this.$dayjs(date).locale("th").format("DD MMM");
                            const year = parseInt(this.$dayjs(date).locale("th").format("YYYY")) + 543;
                            return `${dm} ${year}`;
                        } else return this.$dayjs(date).locale('en').format("DD MMM YYYY");
                    }
                },
                parse: (value) => {
                    if (!value) return null;
                    else {
                        if (this.$i18n.locale === "th") {
                            const dmy = value.split(" ");
                            let year = parseInt(dmy[2]);
                            let month = 1;
                            const monthth = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
                            year -= 543;
                            month = monthth.findIndex((item) => dmy[1] === item);
                            if (month !== -1) month = month + 1;
                            return this.$dayjs(`${year}-${month}-${dmy[0]}`, "YYYY-M-DD").toDate();
                        } else return this.$dayjs(value, "DD MMM YYYY").toDate();

                    }
                },
            },
            yearFormat: {
                stringify: (date) => {
                    
                    if (!date) return "";
                    else {
                        if (this.$i18n.locale === "th") {
                            const dm = this.$dayjs(date).locale("th").format("DD MMM");
                            const year = parseInt(this.$dayjs(date).locale("th").format("YYYY")) + 543;
                            return `${year}`;
                        } else return this.$dayjs(date).locale('en').format("YYYY");
                    }
                },
                parse: (value) => {
                    
                    if (!value) return null;
                    else {
                        if (this.$i18n.locale === "th") {
                            const dmy = value.split(" ");
                            let year = parseInt(dmy[2]);
                            let month = 1;
                            const monthth = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
                            year -= 543;
                            month = monthth.findIndex((item) => dmy[1] === item);
                            if (month !== -1) month = month + 1;
                            return this.$dayjs(`${year}-${month}-${dmy[0]}`, "YYYY-M-DD").toDate();
                        } else return this.$dayjs(value, "DD MMM YYYY").toDate();

                    }
                },
            },
            monthFormat: {
                stringify: (date) => {
                    
                    if (!date) return "";
                    else {
                        if (this.$i18n.locale === "th") {
                            const dm = this.$dayjs(date).locale("th").format("MMMM");
                            const year = parseInt(this.$dayjs(date).locale("th").format("YYYY")) + 543;
                            return `${dm} ${year}`;
                        } else return this.$dayjs(date).locale('en').format("MMMM YYYY");
                    }
                },
                parse: (value) => {
                    
                    if (!value) return null;
                    else {
                        if (this.$i18n.locale === "th") {
                            const dmy = value.split(" ");
                            let year = parseInt(dmy[2]);
                            let month = 1;
                            const monthth = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
                            year -= 543;
                            month = monthth.findIndex((item) => dmy[1] === item);
                            if (month !== -1) month = month + 1;
                            return this.$dayjs(`${year}-${month}-${dmy[0]}`, "YYYY-M-DD").toDate();
                        } else return this.$dayjs(value, "DD MMM YYYY").toDate();

                    }
                },
            },
        }
    }
}