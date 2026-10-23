# scripts/enrich_vue_service_detail.py
import sys
import os
import json
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.enrich_seo_data import ENRICHMENTS

vue_file = 'frontend/src/pages/ServiceDetailPage.vue'
with open(vue_file, 'r', encoding='utf-8') as f:
    vue_code = f.read()

# 1. Update each service in servicesMap by injecting problemsRu, problemsKz, problemsEn, knowsAbout
for slug, extra in ENRICHMENTS.items():
    # Find service in vue_code: e.g. '"mcc-cabinets": {'
    target = f'"{slug}": {{'
    pos = vue_code.find(target)
    if pos == -1:
        target = f"'{slug}': {{"
        pos = vue_code.find(target)
    if pos == -1:
        print(f"Warning: could not find {slug} in ServiceDetailPage.vue")
        continue

    # Let's inject after the target line: knowsAbout, problemsRu, problemsKz, problemsEn
    ru_problems = extra['ru'].get('problems', [])
    kz_problems = extra['kz'].get('problems', [])
    en_problems = extra['en'].get('problems', [])
    knows_about = extra.get('knowsAbout', [])
    extra_faqs_ru = extra['ru'].get('faqs', [])
    extra_faqs_kz = extra['kz'].get('faqs', [])
    extra_faqs_en = extra['en'].get('faqs', [])

    injection = f"""
    knowsAbout: {json.dumps(knows_about, ensure_ascii=False)},
    problemsRu: {json.dumps(ru_problems, ensure_ascii=False, indent=6)},
    problemsKz: {json.dumps(kz_problems, ensure_ascii=False, indent=6)},
    problemsEn: {json.dumps(en_problems, ensure_ascii=False, indent=6)},
    faqsKz: {json.dumps(extra_faqs_kz, ensure_ascii=False, indent=6)},
    faqsEn: {json.dumps(extra_faqs_en, ensure_ascii=False, indent=6)},"""

    # Check if already injected
    if f'"{slug}": {{\n    knowsAbout:' not in vue_code and f'"{slug}": {{\r\n    knowsAbout:' not in vue_code:
        vue_code = vue_code[:pos + len(target)] + injection + vue_code[pos + len(target):]
        print(f"Injected problems and metadata for {slug}")

# 2. Add computed properties for serviceProblems, serviceFaqs, serviceStages
computed_target = 'const serviceFeatures = computed(() => {'
computed_addition = '''const serviceProblems = computed(() => {
  const s = currentService.value;
  if (!s) return [];
  if (activeLang.value === "kz" && s.problemsKz && s.problemsKz.length) return s.problemsKz;
  if (activeLang.value === "en" && s.problemsEn && s.problemsEn.length) return s.problemsEn;
  return s.problemsRu || [];
});

const serviceFaqs = computed(() => {
  const s = currentService.value;
  if (!s) return [];
  if (activeLang.value === "kz" && s.faqsKz && s.faqsKz.length) return s.faqsKz;
  if (activeLang.value === "en" && s.faqsEn && s.faqsEn.length) return s.faqsEn;
  return s.faqsRu || [];
});

const serviceStages = computed(() => {
  const s = currentService.value;
  if (!s) return [];
  if (activeLang.value === "kz" && s.stagesKz && s.stagesKz.length) return s.stagesKz;
  if (activeLang.value === "en" && s.stagesEn && s.stagesEn.length) return s.stagesEn;
  return s.stagesRu || [];
});

'''

if 'const serviceProblems = computed' not in vue_code:
    pos = vue_code.find(computed_target)
    if pos != -1:
        vue_code = vue_code[:pos] + computed_addition + vue_code[pos:]
        print("Injected serviceProblems, serviceFaqs, serviceStages computed properties")

# 3. Update uiLabels with problems and problemsTitle
ui_target = 'capabilitiesTitle: l === "kz" ? "Жүйені енгізуге не кіреді" : (l === "en" ? "System Scope & Deliverables" : "Что входит в реализацию системы"),'
ui_replacement = '''capabilitiesTitle: l === "kz" ? "Жүйені енгізуге не кіреді" : (l === "en" ? "System Scope & Deliverables" : "Что входит в реализацию системы"),
    problems: l === "kz" ? "Мәселелер мен шешімдер" : (l === "en" ? "Challenges & Solutions" : "Задачи и решения"),
    problemsTitle: l === "kz" ? "Нысандағы жиі кездесетін мәселелерді қалай шешеміз" : (l === "en" ? "How We Solve Field Engineering Challenges" : "Решаемые задачи и симптомы на объекте"),'''

if 'problemsTitle:' not in vue_code and ui_target in vue_code:
    vue_code = vue_code.replace(ui_target, ui_replacement, 1)
    print("Injected problems labels to uiLabels")

# 4. In applySeo, inject knowsAbout and FAQPage schema
seo_target = '    {\n      "@context": "https://schema.org",\n      "@type": "Service",\n      "name": serviceTitle.value,\n      "description": serviceDesc.value,\n      "provider": {'
seo_replacement = '''    {
      "@context": "https://schema.org",
      "@type": "Service",
      "name": serviceTitle.value,
      "description": serviceDesc.value,
      "knowsAbout": (service.knowsAbout || []).map(k => ({
        "@type": "DefinedTerm",
        "name": k.name,
        "sameAs": k.sameAs
      })),
      "provider": {'''

if '"knowsAbout": (service.knowsAbout' not in vue_code and seo_target in vue_code:
    vue_code = vue_code.replace(seo_target, seo_replacement, 1)
    print("Injected knowsAbout to Service schema in applySeo")

seo_faq_target = '    {\n      "@context": "https://schema.org",\n      "@type": "BreadcrumbList",'
seo_faq_replacement = '''    ...(serviceFaqs.value.length ? [{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": serviceFaqs.value.map(f => ({
        "@type": "Question",
        "name": f.q,
        "acceptedAnswer": { "@type": "Answer", "text": f.a }
      }))
    }] : []),
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",'''

if '@type": "FAQPage"' not in vue_code and seo_faq_target in vue_code:
    vue_code = vue_code.replace(seo_faq_target, seo_faq_replacement, 1)
    print("Injected FAQPage to applySeo")

# 5. In template: insert Problems section right after Capabilities section
template_cap_end = '        </div>\n      </section>\n\n      <!-- Этапы работ -->'
template_problems_block = '''        </div>
      </section>

      <!-- Решаемые задачи и инженерные решения (Problem-Solution Matrix) -->
      <section v-if="serviceProblems.length" class="max-w-7xl mx-auto px-6 lg:px-12 mb-20">
        <div class="flex items-center gap-4 mb-4">
          <div class="h-px w-8 bg-amber-500" />
          <span class="text-amber-500 text-xs uppercase tracking-[0.2em] font-medium">{{ uiLabels.problems }}</span>
        </div>
        <h2 class="text-2xl md:text-3xl font-light tracking-tight text-white mb-8">
          {{ uiLabels.problemsTitle }}
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div
            v-for="(p, pIdx) in serviceProblems"
            :key="pIdx"
            class="p-6 border border-[#333842] bg-[#1A1D23]/70 rounded-xl hover:border-amber-500/40 transition-all duration-300 flex flex-col justify-between"
          >
            <div>
              <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-medium mb-4">
                <span>⚠️ {{ activeLang === 'kz' ? 'Нысандағы мәселе' : (activeLang === 'en' ? 'Field Problem' : 'Проблема на объекте') }}</span>
              </div>
              <h3 class="text-sm font-normal text-white mb-4 leading-relaxed">
                {{ p.problem }}
              </h3>
              <div class="p-3.5 rounded-lg bg-[#252932]/70 border border-[#333842] text-xs text-[#D1D5DB] mb-4 leading-relaxed">
                <span class="text-[#60A5FA] font-medium block mb-1">🛠️ {{ activeLang === 'kz' ? 'INPAR инженерлік шешімі' : (activeLang === 'en' ? 'INPAR Engineering Solution' : 'Инженерное решение INPAR') }}:</span>
                {{ p.solution }}
              </div>
            </div>
            <div class="pt-3 border-t border-[#333842]/50 text-xs text-emerald-400 font-medium flex items-start gap-2">
              <span class="shrink-0">✅</span>
              <span>{{ p.benefit }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Этапы работ -->'''

if '<!-- Решаемые задачи и инженерные решения' not in vue_code and template_cap_end in vue_code:
    vue_code = vue_code.replace(template_cap_end, template_problems_block, 1)
    print("Injected Problems section into template")

# 6. In template: update stages and faqs loops to use serviceStages and serviceFaqs
vue_code = vue_code.replace('v-if="currentService.stagesRu && currentService.stagesRu.length"', 'v-if="serviceStages.length"')
vue_code = vue_code.replace('v-for="(stage, idx) in currentService.stagesRu"', 'v-for="(stage, idx) in serviceStages"')
vue_code = vue_code.replace('v-if="currentService.faqsRu && currentService.faqsRu.length"', 'v-if="serviceFaqs.length"')
vue_code = vue_code.replace('v-for="(faq, fIdx) in currentService.faqsRu"', 'v-for="(faq, fIdx) in serviceFaqs"')

with open(vue_file, 'w', encoding='utf-8') as f:
    f.write(vue_code)

print("Saved updated frontend/src/pages/ServiceDetailPage.vue!")
