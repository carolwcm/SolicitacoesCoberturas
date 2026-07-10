<template>
  <div class="space-y-6">
    <!-- Header Area -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-100 no-print">
      <div>
        <h1 class="text-2xl font-bold text-slate-800 tracking-tight">Relatórios CCIRAS/Farmácia</h1>
        <p class="text-sm text-slate-500 mt-1">Análise de indicadores, produtividade, economia e SLA de avaliações.</p>
      </div>

      <!-- Tab Buttons -->
      <div class="flex bg-slate-50 p-1 rounded-xl border border-slate-100">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            activeTab === tab.id 
              ? 'bg-white text-indigo-750 shadow-sm border-slate-200' 
              : 'text-slate-500 hover:text-slate-800 hover:bg-slate-100/50',
            'px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 cursor-pointer'
          ]"
        >
          {{ tab.name }}
        </button>
      </div>
    </div>

    <!-- Filters Panel -->
    <div class="flex flex-col md:flex-row gap-4 items-center justify-between bg-white p-4 rounded-2xl shadow-sm border border-slate-100 no-print">
      <div class="flex flex-wrap items-center gap-4 w-full md:w-auto">
        <!-- Period Filter -->
        <div class="flex items-end gap-2 flex-wrap">
          <div class="flex flex-col">
            <label class="text-xs font-bold text-slate-400 uppercase mb-1">Período</label>
            <select 
              v-model="filtroPeriodo" 
              class="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm text-slate-700 font-semibold focus:outline-none focus:border-indigo-650 cursor-pointer min-w-[150px]"
            >
              <option value="todos">Todos</option>
              <option value="7d">Últimos 7 dias</option>
              <option value="30d">Últimos 30 dias</option>
              <option value="mes">Mês atual</option>
              <option value="personalizado">Personalizado</option>
            </select>
          </div>

          <div v-if="filtroPeriodo === 'personalizado'" class="flex items-center gap-2 flex-wrap">
            <div class="flex flex-col">
              <label class="text-xs font-bold text-slate-400 uppercase mb-1">Início</label>
              <input 
                v-model="dataInicial" 
                type="date" 
                class="bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-sm text-slate-750 font-semibold focus:outline-none focus:border-indigo-650 cursor-pointer animate-fade-in"
              >
            </div>
            <div class="flex flex-col">
              <label class="text-xs font-bold text-slate-400 uppercase mb-1">Fim</label>
              <input 
                v-model="dataFinal" 
                type="date" 
                class="bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-sm text-slate-750 font-semibold focus:outline-none focus:border-indigo-650 cursor-pointer animate-fade-in"
              >
            </div>
          </div>
        </div>

        <!-- Unit Filter -->
        <div class="flex flex-col">
          <label class="text-xs font-bold text-slate-400 uppercase mb-1">Unidade Funcional</label>
          <select 
            v-model="filtroUnidade" 
            class="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm text-slate-700 font-semibold focus:outline-none focus:border-indigo-650 cursor-pointer min-w-[180px]"
          >
            <option value="todas">Todas</option>
            <option value="UTI Adulto">UTI Adulto</option>
            <option value="Clínica Médica">Clínica Médica</option>
            <option value="Clínica Cirúrgica">Clínica Cirúrgica</option>
            <option value="Emergência">Emergência</option>
            <option value="Ortopedia">Ortopedia</option>
            <option value="Pediatria">Pediatria</option>
            <option value="Oncologia">Oncologia</option>
          </select>
        </div>
      </div>

      <!-- Export Button with Dropdown -->
      <div class="relative">
        <button 
          @click="toggleExportDropdown"
          class="flex items-center gap-2 bg-[#009688] hover:bg-[#00796B] text-white font-semibold px-4 py-2.5 rounded-xl text-sm transition-all shadow-sm cursor-pointer"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          <span>Exportar</span>
        </button>

        <!-- Backdrop to close dropdown -->
        <div v-if="showExportDropdown" @click="showExportDropdown = false" class="fixed inset-0 z-20 bg-transparent no-print"></div>

        <!-- Dropdown Menu -->
        <div v-if="showExportDropdown" class="absolute right-0 mt-2 w-48 bg-white border border-slate-100 rounded-xl shadow-xl z-30 py-1 no-print">
          <button 
            @click="acaoExportar('print')"
            class="flex items-center gap-2 w-full text-left px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 font-semibold cursor-pointer"
          >
            <svg class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
            </svg>
            Imprimir
          </button>
          <button 
            @click="acaoExportar('pdf')"
            class="flex items-center gap-2 w-full text-left px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 font-semibold cursor-pointer"
          >
            <svg class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            Exportar para .pdf
          </button>
          <button 
            @click="acaoExportar('csv')"
            class="flex items-center gap-2 w-full text-left px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 font-semibold cursor-pointer"
          >
            <svg class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Exportar para .csv
          </button>
        </div>
      </div>
    </div>

    <!-- TAB 1: VISÃO GERAL -->
    <div v-if="activeTab === 'geral'" class="space-y-6">
      <!-- Upper Metrics Row -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
        <!-- Metric Cards -->
        <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex items-center space-x-4">
          <div class="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div>
            <p class="text-xs font-semibold text-slate-400 uppercase">Solicitações</p>
            <p class="text-2xl font-extrabold text-slate-800">{{ totalCount }}</p>
          </div>
        </div>

        <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex items-center space-x-4">
          <div class="p-3 bg-emerald-50 text-emerald-600 rounded-xl">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-xs font-semibold text-slate-400 uppercase">Autorizadas</p>
            <p class="text-2xl font-extrabold text-slate-800">{{ autorizadasCount }}</p>
            <p class="text-[10px] text-slate-400 font-semibold">{{ pctAutorizadas }}% do total</p>
          </div>
        </div>

        <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex items-center space-x-4">
          <div class="p-3 bg-rose-50 text-rose-600 rounded-xl">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-xs font-semibold text-slate-400 uppercase">Itens Negados</p>
            <p class="text-2xl font-extrabold text-slate-800">{{ negadasCount }}</p>
            <p class="text-[10px] text-slate-400 font-semibold">{{ pctNegadas }}% do total</p>
          </div>
        </div>

        <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex items-center space-x-4">
          <div class="p-3 bg-blue-50 text-blue-600 rounded-xl">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-xs font-semibold text-slate-400 uppercase">Em análise</p>
            <p class="text-2xl font-extrabold text-slate-800">{{ emAnaliseCount }}</p>
            <p class="text-[10px] text-slate-400 font-semibold">{{ pctEmAnalise }}% do total</p>
          </div>
        </div>

        <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex items-center space-x-4">
          <div class="p-3 bg-teal-50 text-teal-600 rounded-xl">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
          </div>
          <div>
            <p class="text-xs font-semibold text-slate-400 uppercase">Liberadas Farmácia</p>
            <p class="text-2xl font-extrabold text-slate-800">{{ liberadasCount }}</p>
            <p class="text-[10px] text-slate-400 font-semibold">{{ pctLiberadas }}% do total</p>
          </div>
        </div>

        <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex items-center space-x-4">
          <div class="p-3 bg-violet-50 text-violet-600 rounded-xl">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-xs font-semibold text-slate-400 uppercase">Tempo Médio Resposta</p>
            <p class="text-2xl font-extrabold text-slate-800">{{ tempoMedioResposta }}</p>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Chart 1: Line Chart (Monthly Requests) -->
        <!-- Chart 1: Line Chart (Monthly Requests) -->
        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between">
          <h3 class="text-sm font-bold text-slate-700 mb-4">Solicitações por mês</h3>
          <div class="h-64 relative border-l border-b border-slate-100 w-full mt-4 flex items-end justify-between px-2 pt-6">
            <!-- Dynamic SVG Line Graph -->
            <svg class="absolute inset-0 h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none">
              <!-- Gradient definition -->
              <defs>
                <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="rgba(0, 150, 136, 0.3)" />
                  <stop offset="100%" stop-color="rgba(0, 150, 136, 0)" />
                </linearGradient>
              </defs>
              <!-- Grid lines for clean look -->
              <line x1="10" y1="20" x2="90" y2="20" stroke="#f1f5f9" stroke-width="0.5" stroke-dasharray="2" />
              <line x1="10" y1="45" x2="90" y2="45" stroke="#f1f5f9" stroke-width="0.5" stroke-dasharray="2" />
              <line x1="10" y1="70" x2="90" y2="70" stroke="#f1f5f9" stroke-width="0.5" stroke-dasharray="2" />
              
              <!-- Area under curve -->
              <path :d="areaPathD" fill="url(#chartGradient)" />
              <!-- Path line -->
              <path :d="pathD" fill="none" stroke="#009688" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              <!-- Circles for each point -->
              <circle v-for="pt in pontosGrafico" :key="'c-' + pt.label" :cx="pt.x" :cy="pt.y" r="2" fill="#009688" stroke="white" stroke-width="0.5" />
            </svg>
            
            <!-- Monthly label overlays -->
            <div 
              v-for="pt in pontosGrafico" 
              :key="'l-' + pt.label" 
              class="text-[10px] text-slate-400 absolute bottom-1 font-semibold animate-fade-in" 
              :style="{ left: `${pt.x}%`, transform: 'translateX(-50%)' }"
            >
              {{ pt.label }}
            </div>
            
            <!-- Value badge overlays -->
            <div 
              v-for="pt in pontosGrafico" 
              :key="'b-' + pt.label" 
              class="absolute text-[9px] font-bold bg-[#009688] text-white px-1.5 py-0.5 rounded shadow-sm no-print transition-all duration-300"
              :style="{ left: `${pt.x}%`, top: `calc(${pt.y}% - 14px)`, transform: 'translateX(-50%)' }"
            >
              {{ pt.count }}
            </div>
          </div>
        </div>

        <!-- Chart 2: Status Donut Chart -->
        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between">
          <h3 class="text-sm font-bold text-slate-700 mb-4">Status das solicitações</h3>
          <div class="flex items-center justify-around flex-1">
            <!-- SVG Donut Chart -->
            <div class="relative w-36 h-36">
              <svg class="w-full h-full transform -rotate-90" viewBox="0 0 40 40">
                <!-- Outer circle representing different slices -->
                <circle class="text-slate-100" stroke="currentColor" stroke-width="4" fill="none" cx="20" cy="20" r="15.915" />
                <circle class="text-emerald-500" :stroke-dasharray="`${pctAutorizadas} ${100 - pctAutorizadas}`" stroke-dashoffset="0" stroke="currentColor" stroke-width="4.5" fill="none" cx="20" cy="20" r="15.915" />
                <circle class="text-rose-500" :stroke-dasharray="`${pctNegadas} ${100 - pctNegadas}`" :stroke-dashoffset="`-${pctAutorizadas}`" stroke="currentColor" stroke-width="4.5" fill="none" cx="20" cy="20" r="15.915" />
                <circle class="text-indigo-500" :stroke-dasharray="`${pctEmAnalise} ${100 - pctEmAnalise}`" :stroke-dashoffset="`-${pctAutorizadas + pctNegadas}`" stroke="currentColor" stroke-width="4.5" fill="none" cx="20" cy="20" r="15.915" />
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
                <span class="text-2xl font-black text-slate-800">{{ totalCount }}</span>
                <span class="text-[9px] font-bold text-slate-400 uppercase">Total</span>
              </div>
            </div>
            <!-- Labels -->
            <div class="space-y-2 text-xs">
              <div class="flex items-center"><span class="w-3 h-3 bg-emerald-500 rounded-full mr-2"></span> {{ autorizadasCount }} Autorizadas</div>
              <div class="flex items-center"><span class="w-3 h-3 bg-rose-500 rounded-full mr-2"></span> {{ negadasCount }} Negadas</div>
              <div class="flex items-center"><span class="w-3 h-3 bg-indigo-500 rounded-full mr-2"></span> {{ emAnaliseCount }} Em análise</div>
              <div class="flex items-center"><span class="w-3 h-3 bg-slate-400 rounded-full mr-2"></span> {{ pendentesCount }} Pendentes</div>
            </div>
          </div>
        </div>

        <!-- Chart 3: Top 10 requested covers -->
        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
          <h3 class="text-sm font-bold text-slate-700 mb-4">Top Coberturas solicitadas</h3>
          <div class="space-y-3">
            <div v-for="item in topMaterials" :key="item.name" class="space-y-1">
              <div class="flex justify-between text-xs font-semibold text-slate-600">
                <span class="truncate max-w-[200px]">{{ item.name }}</span>
                <span>{{ item.count }}</span>
              </div>
              <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                <div class="bg-indigo-650 h-full rounded-full" :style="{ width: `${(item.count / maxMaterialCount) * 100}%` }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: INDICADORES DE QUALIDADE -->
    <div v-if="activeTab === 'qualidade'" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <!-- Quality Cards -->
        <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
          <p class="text-xs font-bold text-slate-400 uppercase mb-2">Taxa de aprovação</p>
          <p class="text-3xl font-black text-indigo-750">{{ pctAprovacao }}%</p>
          <div class="w-full bg-slate-100 h-2.5 rounded-full mt-3 overflow-hidden">
            <div class="bg-emerald-500 h-full rounded-full" :style="{ width: `${pctAprovacao}%` }"></div>
          </div>
          <p class="text-[10px] text-slate-400 mt-2 font-medium">{{ autorizadasCount }} autorizadas de {{ totalCount }} solicitações</p>
        </div>

        <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-slate-400 uppercase mb-2">Tempo médio de avaliação (CCIRAS)</p>
            <p class="text-3xl font-black text-slate-800">{{ tempoMedioResposta }}</p>
          </div>
          <div class="flex items-center gap-2 mt-4 text-emerald-600 text-xs font-bold bg-emerald-50 py-1.5 px-3 rounded-xl w-fit">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
            </svg>
            <span>Meta: até 24h</span>
          </div>
        </div>

        <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-slate-400 uppercase mb-2">Tempo médio de liberação (Farmácia)</p>
            <p class="text-3xl font-black text-slate-800">{{ tempoMedioFarmacia }}</p>
          </div>
          <div class="flex items-center gap-2 mt-4 text-emerald-600 text-xs font-bold bg-emerald-50 py-1.5 px-3 rounded-xl w-fit">
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
            </svg>
            <span>Meta: até 6h</span>
          </div>
        </div>

        <div class="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
          <p class="text-xs font-bold text-slate-400 uppercase mb-2">Taxa de retrabalho / divergência</p>
          <p class="text-3xl font-black text-slate-800">{{ pctRetrabalho }}%</p>
          <div class="w-full bg-slate-100 h-2.5 rounded-full mt-3 overflow-hidden">
            <div class="bg-rose-500 h-full rounded-full" :style="{ width: `${pctRetrabalho}%` }"></div>
          </div>
          <p class="text-[10px] text-slate-400 mt-2 font-medium">Itens alterados nas auditorias</p>
        </div>
      </div>

      <!-- SLA Details -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- SLA Distribution chart -->
        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col h-full justify-between">
          <h3 class="text-sm font-bold text-slate-700 mb-4">SLA das solicitações (tempo de avaliação)</h3>
          <div class="flex-1 flex items-center justify-around py-4">
            <!-- Pie/Donut SLA -->
            <div class="relative w-36 h-36 shrink-0">
              <svg class="w-full h-full transform -rotate-90" viewBox="0 0 40 40">
                <circle class="text-slate-100" stroke="currentColor" stroke-width="6" fill="none" cx="20" cy="20" r="15.915" />
                <circle class="text-indigo-600" :stroke-dasharray="`${slaRanges.ok} ${100 - slaRanges.ok}`" stroke="currentColor" stroke-width="6" fill="none" cx="20" cy="20" r="15.915" />
                <circle class="text-emerald-500" :stroke-dasharray="`${slaRanges.warning} ${100 - slaRanges.warning}`" :stroke-dashoffset="`-${slaRanges.ok}`" stroke="currentColor" stroke-width="6" fill="none" cx="20" cy="20" r="15.915" />
                <circle class="text-amber-500" :stroke-dasharray="`${slaRanges.late} ${100 - slaRanges.late}`" :stroke-dashoffset="`-${slaRanges.ok + slaRanges.warning}`" stroke="currentColor" stroke-width="6" fill="none" cx="20" cy="20" r="15.915" />
                <circle class="text-rose-500" :stroke-dasharray="`${slaRanges.veryLate} ${100 - slaRanges.veryLate}`" :stroke-dashoffset="`-${slaRanges.ok + slaRanges.warning + slaRanges.late}`" stroke="currentColor" stroke-width="6" fill="none" cx="20" cy="20" r="15.915" />
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
                <span class="text-2xl font-black text-slate-800">{{ filteredSolicitacoes.length }}</span>
                <span class="text-[9px] font-bold text-slate-400 uppercase">
                  {{ filteredSolicitacoes.length === 1 ? 'Avaliação' : 'Avaliações' }}
                </span>
              </div>
            </div>
            <div class="space-y-3 text-xs ml-4 font-semibold text-slate-600">
              <div class="flex items-center"><span class="w-3.5 h-3.5 bg-indigo-600 rounded-full mr-2.5"></span> Até 24h</div>
              <div class="flex items-center"><span class="w-3.5 h-3.5 bg-emerald-500 rounded-full mr-2.5"></span> 24h - 48h</div>
              <div class="flex items-center"><span class="w-3.5 h-3.5 bg-amber-500 rounded-full mr-2.5"></span> 48h - 72h</div>
              <div class="flex items-center"><span class="w-3.5 h-3.5 bg-rose-500 rounded-full mr-2.5"></span> > 72h</div>
            </div>
          </div>
        </div>

        <!-- SLA by unit table -->
        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col h-full justify-between">
          <h3 class="text-sm font-bold text-slate-700 mb-4">Tempo médio de avaliação por unidade</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-slate-100 text-sm">
              <thead>
                <tr class="text-left text-xs font-bold text-slate-400 uppercase">
                  <th class="py-3">Unidade</th>
                  <th class="py-3">Tempo médio</th>
                  <th class="py-3 text-right">SLA Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="unit in slaUnits" :key="unit.name" class="text-slate-600 font-medium">
                  <td class="py-3.5">{{ unit.name }}</td>
                  <td class="py-3.5">{{ unit.time }}</td>
                  <td class="py-3.5 text-right">
                    <span :class="unit.badgeClass">{{ unit.status }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: AUDITORIA E RASTREABILIDADE -->
    <div v-if="activeTab === 'linha'" class="space-y-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm space-y-4">
        <!-- Search bar -->
<<<<<<< Updated upstream
        <div class="no-print relative">
=======
        <div class="no-print">
>>>>>>> Stashed changes
          <label class="block text-sm font-bold text-slate-700 mb-2">Nº da RM ou Nome do Paciente</label>
          <div class="relative max-w-md">
            <input 
              v-model="searchQuery" 
              @focus="focusSuggestions = true"
              @blur="setTimeout(() => focusSuggestions = false, 200)"
              type="text" 
              placeholder="Ex: 1 ou João Silva"
<<<<<<< Updated upstream
              class="w-full border border-slate-200 bg-white rounded-xl py-2.5 pl-4 pr-10 text-sm focus:outline-none focus:border-indigo-650"
=======
              class="w-full border border-slate-200 rounded-xl py-2.5 pl-4 pr-10 text-sm focus:outline-none focus:border-indigo-650"
>>>>>>> Stashed changes
            >
            <button class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>

          <!-- Suggestions Dropdown -->
          <div v-if="focusSuggestions && searchSuggestions.length > 0" class="absolute left-0 mt-1 w-full max-w-md bg-white border border-slate-150 rounded-xl shadow-xl z-50 py-1.5 no-print">
            <button 
              v-for="s in searchSuggestions" 
              :key="s.id"
              type="button"
              @mousedown="selecionarSolicitacaoTrace(s)"
              class="w-full text-left px-4 py-2 hover:bg-slate-50 flex flex-col justify-between transition duration-150 cursor-pointer border-b last:border-0 border-slate-100"
            >
              <div class="flex justify-between text-xs font-bold text-indigo-700">
                <span>RM #{{ s.id }}</span>
                <span class="text-slate-400 font-semibold">{{ s.created_at ? new Date(s.created_at).toLocaleDateString('pt-BR') : '' }}</span>
              </div>
              <div class="text-sm font-bold text-slate-800 mt-0.5">{{ s.nome_paciente }}</div>
              <div class="text-xs text-slate-500 mt-0.5">Prontuário: {{ s.prontuario }} • Status: {{ s.status }}</div>
            </button>
          </div>
        </div>

        <div v-if="loadingTrace" class="py-12 flex justify-center">
          <LoadingIndicator />
        </div>
        
        <div v-else-if="!traceSolicitacao" class="py-8 text-center text-slate-400 font-medium">
          Nenhuma solicitação selecionada ou encontrada com a busca. Digite e selecione para buscar a linha do tempo completa.
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
          <!-- Timeline -->
          <div class="md:col-span-1 border border-slate-100 rounded-2xl p-5 bg-slate-50/50">
            <h4 class="font-bold text-slate-700 mb-4">Auditoria e rastreabilidade</h4>
            <div class="space-y-6 relative border-l-2 border-indigo-600 ml-4 pl-6">
              <div v-for="step in traceSteps" :key="step.title" class="relative">
                <!-- Checkpoint Circle -->
                <div class="absolute -left-10 top-0.5 w-6 h-6 rounded-full bg-white border-4 border-indigo-600 flex items-center justify-center">
                  <div class="w-1.5 h-1.5 bg-indigo-600 rounded-full"></div>
                </div>
                <div>
                  <p class="text-xs text-slate-400 font-bold">{{ step.date }}</p>
                  <p class="text-sm font-bold text-slate-800">{{ step.title }}</p>
                  <p class="text-xs text-slate-500 font-medium">{{ step.actor }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Solicitation data and actions table -->
          <div class="md:col-span-2 space-y-6">
            <div class="border border-slate-100 rounded-2xl p-5 bg-white space-y-3">
              <h4 class="font-bold text-slate-700 border-b pb-2">Dados da solicitação</h4>
              <div class="grid grid-cols-2 gap-4 text-sm text-slate-650 font-medium">
                <div><span class="text-slate-400 block text-xs">Paciente:</span> {{ traceSolicitacao.nome_paciente }}</div>
                <div><span class="text-slate-400 block text-xs">Prontuário:</span> {{ traceSolicitacao.prontuario }}</div>
                <div><span class="text-slate-400 block text-xs">Unidade solicitante:</span> {{ traceSolicitacao.leito ? 'Ala Curativos' : 'Unidade Geral' }}</div>
                <div><span class="text-slate-400 block text-xs">Leito:</span> {{ traceSolicitacao.leito || 'N/A' }}</div>
                <div><span class="text-slate-400 block text-xs">Item solicitado:</span> {{ traceSolicitacao.itens[0]?.nome_material }}</div>
                <div><span class="text-slate-400 block text-xs">Quantidade:</span> {{ traceSolicitacao.itens[0]?.quantidade_solicitada }} unidade(s)</div>
              </div>
            </div>

            <!-- Action logs table -->
            <div class="border border-slate-100 rounded-2xl p-5 bg-white">
              <h4 class="font-bold text-slate-700 mb-3 border-b pb-2">Histórico de ações</h4>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-slate-100 text-xs text-slate-600">
                  <thead class="bg-slate-50 text-slate-400 font-bold uppercase">
                    <tr>
                      <th class="py-2.5 px-3 text-left">Data/Hora</th>
                      <th class="py-2.5 px-3 text-left">Usuário</th>
                      <th class="py-2.5 px-3 text-left">Setor</th>
                      <th class="py-2.5 px-3 text-left">Ação</th>
                      <th class="py-2.5 px-3 text-left">Observação</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100">
                    <tr v-for="action in actionHistory" :key="action.time" class="hover:bg-slate-50/50">
                      <td class="py-3 px-3 font-semibold">{{ action.time }}</td>
                      <td class="py-3 px-3 font-semibold">{{ action.user }}</td>
                      <td class="py-3 px-3 font-semibold">{{ action.sector }}</td>
                      <td class="py-3 px-3 font-semibold">
                        <span :class="action.actionBadge">{{ action.action }}</span>
                      </td>
                      <td class="py-3 px-3 italic">{{ action.note }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import SolicitacoesService, { SolicitacaoCobertura } from '../services/SolicitacoesService';
import LoadingIndicator from '../components/LoadingIndicator.vue';

const activeTab = ref('geral');
const loading = ref(false);
const solicitacoes = ref<SolicitacaoCobertura[]>([]);

// Filters
const filtroPeriodo = ref('todos');
const dataInicial = ref('');
const dataFinal = ref('');
const filtroUnidade = ref('todas');

const tabs = [
  { id: 'geral', name: 'Visão Geral' },
  { id: 'qualidade', name: 'Indicadores de Qualidade' },
  { id: 'linha', name: 'Auditoria e rastreabilidade' }
];

// Load all solicitations data on mount
const loadData = async () => {
  loading.value = true;
  try {
    solicitacoes.value = await SolicitacoesService.listar();
  } catch (err) {
    console.error('Failed to load dashboard report data:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadData();
});

// Dynamic filtering of solicitations
const filteredSolicitacoes = computed(() => {
  let list = solicitacoes.value;

  // Filter by Unit Functional
  if (filtroUnidade.value !== 'todas') {
    list = list.filter(s => {
      if (!s.leito) return false;
      return s.leito.toLowerCase().includes(filtroUnidade.value.toLowerCase());
    });
  }

  // Filter by Period
  if (filtroPeriodo.value !== 'todos') {
    const now = new Date();
    list = list.filter(s => {
      if (!s.created_at) return false;
      const date = new Date(s.created_at);
      if (filtroPeriodo.value === '7d') {
        const diffTime = Math.abs(now.getTime() - date.getTime());
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays <= 7;
      }
      if (filtroPeriodo.value === '30d') {
        const diffTime = Math.abs(now.getTime() - date.getTime());
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays <= 30;
      }
      if (filtroPeriodo.value === 'mes') {
        return date.getMonth() === now.getMonth() && date.getFullYear() === now.getFullYear();
      }
      if (filtroPeriodo.value === 'personalizado') {
        if (dataInicial.value) {
          const start = new Date(dataInicial.value + 'T00:00:00');
          if (date < start) return false;
        }
        if (dataFinal.value) {
          const end = new Date(dataFinal.value + 'T23:59:59');
          if (date > end) return false;
        }
        return true;
      }
      return true;
    });
  }

  return list;
});

// Tab 1: General Computations
const totalCount = computed(() => filteredSolicitacoes.value.length || 1); // Avoid division by zero
const autorizadasCount = computed(() => filteredSolicitacoes.value.filter(s => s.status === 'AUTORIZADO' || s.status === 'LIBERADO' || s.status === 'ENTREGUE').length);
const negadasCount = computed(() => filteredSolicitacoes.value.filter(s => s.status === 'NEGADO').length);
const emAnaliseCount = computed(() => filteredSolicitacoes.value.filter(s => s.status === 'EM ANÁLISE').length);
const pendentesCount = computed(() => filteredSolicitacoes.value.filter(s => s.status === 'PENDENTE').length);
const liberadasCount = computed(() => filteredSolicitacoes.value.filter(s => s.status === 'LIBERADO' || s.status === 'ENTREGUE').length);

const pctAutorizadas = computed(() => Math.round((autorizadasCount.value / totalCount.value) * 100) || 0);
const pctNegadas = computed(() => Math.round((negadasCount.value / totalCount.value) * 100) || 0);
const pctEmAnalise = computed(() => Math.round((emAnaliseCount.value / totalCount.value) * 100) || 0);
const pctLiberadas = computed(() => Math.round((liberadasCount.value / totalCount.value) * 100) || 0);

const tempoMedioResposta = computed(() => {
  const audited = filteredSolicitacoes.value.filter(s => s.created_at && s.data_auditoria);
  if (audited.length === 0) return 'N/A';
  
  let totalMs = 0;
  audited.forEach(s => {
    const start = new Date(s.created_at!);
    const end = new Date(s.data_auditoria!);
    totalMs += Math.abs(end.getTime() - start.getTime());
  });
  
  const avgMs = totalMs / audited.length;
  const avgMinutes = Math.floor(avgMs / (1000 * 60));
  const hours = Math.floor(avgMinutes / 60);
  const minutes = avgMinutes % 60;
  
  return `${hours}h ${minutes}m`;
});

const tempoMedioFarmacia = computed(() => {
  const delivered = filteredSolicitacoes.value.filter(s => s.data_auditoria && s.data_entrega);
  if (delivered.length === 0) return 'N/A';
  
  let totalMs = 0;
  delivered.forEach(s => {
    const start = new Date(s.data_auditoria!);
    const end = new Date(s.data_entrega!);
    totalMs += Math.abs(end.getTime() - start.getTime());
  });
  
  const avgMs = totalMs / delivered.length;
  const avgMinutes = Math.floor(avgMs / (1000 * 60));
  const hours = Math.floor(avgMinutes / 60);
  const minutes = avgMinutes % 60;
  
  return `${hours}h ${minutes}m`;
});

// Top Materials Computation
const topMaterials = computed(() => {
  const counts: Record<string, number> = {};
  filteredSolicitacoes.value.forEach(s => {
    s.itens.forEach(i => {
      counts[i.nome_material] = (counts[i.nome_material] || 0) + i.quantidade_solicitada;
    });
  });
  const sorted = Object.entries(counts)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);
  
  if (sorted.length === 0) {
    return [
      { name: 'Curativo Hidrocolóide Extra Fino 10x10', count: 46 },
      { name: 'Curativo com Prata Nanocristalina 10x12', count: 32 },
      { name: 'Espuma de Poliuretano com Silicone', count: 18 },
      { name: 'Alginato de Cálcio e Sódio', count: 12 }
    ];
  }
  return sorted;
});

const maxMaterialCount = computed(() => {
  const max = Math.max(...topMaterials.value.map(m => m.count));
  return max || 1;
});

// Gráfico de Solicitações por Mês
const mesesGrafico = computed(() => {
  const months = [];
  const now = new Date();
  // Gerar os últimos 6 meses cronologicamente
  for (let i = 5; i >= 0; i--) {
    const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
    months.push({
      year: d.getFullYear(),
      month: d.getMonth(),
      name: d.toLocaleDateString('pt-BR', { month: 'short' }).replace('.', '').toUpperCase()
    });
  }
  return months;
});

const contagemPorMes = computed(() => {
  const months = mesesGrafico.value;
  return months.map(m => {
    const count = filteredSolicitacoes.value.filter(s => {
      if (!s.created_at) return false;
      const d = new Date(s.created_at);
      return d.getFullYear() === m.year && d.getMonth() === m.month;
    }).length;
    return { ...m, count };
  });
});

const pontosGrafico = computed(() => {
  const data = contagemPorMes.value;
  const maxCount = Math.max(...data.map(d => d.count)) || 1;
  
  return data.map((d, index) => {
    // Distribuir X de 10% a 90%
    const x = 10 + (index / 5) * 80;
    // Y vai de 70% (mínimo / zero) até 20% (máximo / topo)
    const y = 70 - (d.count / maxCount) * 50;
    return { x, y, count: d.count, label: d.name };
  });
});

const pathD = computed(() => {
  const pts = pontosGrafico.value;
  if (pts.length === 0) return '';
  return `M ${pts.map(p => `${p.x} ${p.y}`).join(' L ')}`;
});

const areaPathD = computed(() => {
  const pts = pontosGrafico.value;
  if (pts.length === 0) return '';
  const first = pts[0];
  const last = pts[pts.length - 1];
  return `M ${first.x} 70 L ${pts.map(p => `${p.x} ${p.y}`).join(' L ')} L ${last.x} 70 Z`;
});

// Tab 2: Quality SLA Computations
const pctAprovacao = computed(() => {
  const total = autorizadasCount.value + negadasCount.value;
  if (total === 0) return 0;
  return Math.round((autorizadasCount.value / total) * 100);
});
const pctRetrabalho = computed(() => {
  let totalItens = 0;
  let itensAlterados = 0;
  
  filteredSolicitacoes.value.forEach(s => {
    s.itens.forEach(i => {
      totalItens++;
      if (i.quantidade_autorizada !== undefined && i.quantidade_autorizada !== null && i.quantidade_autorizada !== i.quantidade_solicitada) {
        itensAlterados++;
      }
    });
  });
  
  if (totalItens === 0) return 0;
  return Math.round((itensAlterados / totalItens) * 1000) / 10;
});

const slaRanges = computed(() => {
  let ok = 0;
  let warning = 0;
  let late = 0;
  let veryLate = 0;
  
  const total = filteredSolicitacoes.value.length;
  if (total === 0) {
    return { ok: 100, warning: 0, late: 0, veryLate: 0 };
  }
  
  const now = new Date();
  filteredSolicitacoes.value.forEach(s => {
    if (!s.created_at) {
      ok++;
      return;
    }
    const start = new Date(s.created_at);
    const end = s.data_auditoria ? new Date(s.data_auditoria) : now;
    const diffHours = Math.abs(end.getTime() - start.getTime()) / (1000 * 60 * 60);
    
    if (diffHours <= 24) {
      ok++;
    } else if (diffHours <= 48) {
      warning++;
    } else if (diffHours <= 72) {
      late++;
    } else {
      veryLate++;
    }
  });
  
  return {
    ok: Math.round((ok / total) * 100),
    warning: Math.round((warning / total) * 100),
    late: Math.round((late / total) * 100),
    veryLate: Math.round((veryLate / total) * 100)
  };
});

const slaUnits = computed(() => {
  const units = [
    'UTI Adulto',
    'Clínica Médica',
    'Clínica Cirúrgica',
    'Emergência',
    'Ortopedia',
    'Pediatria',
    'Oncologia'
  ];
  
  const now = new Date();
  
  return units.map(unitName => {
    const unitSols = filteredSolicitacoes.value.filter(s => 
      s.leito && s.leito.toLowerCase().includes(unitName.toLowerCase())
    );
    
    if (unitSols.length === 0) {
      return {
        name: unitName,
        time: 'N/A',
        status: 'Sem dados',
        badgeClass: 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-50 text-slate-400 border border-slate-200'
      };
    }
    
    let totalMs = 0;
    let count = 0;
    unitSols.forEach(s => {
      if (!s.created_at) return;
      const start = new Date(s.created_at);
      const end = s.data_auditoria ? new Date(s.data_auditoria) : now;
      totalMs += Math.abs(end.getTime() - start.getTime());
      count++;
    });
    
    const avgMs = count > 0 ? totalMs / count : 0;
    const avgHours = avgMs / (1000 * 60 * 60);
    
    let timeStr = '0h';
    if (count > 0) {
      const avgMinutes = Math.floor(avgMs / (1000 * 60));
      const hours = Math.floor(avgMinutes / 60);
      const minutes = avgMinutes % 60;
      timeStr = `${hours}h ${minutes}m`;
    }
    
    let status = 'SLA OK';
    let badgeClass = 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
    
    if (avgHours > 24) {
      status = 'SLA Estourado';
      badgeClass = 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200';
    } else if (avgHours > 18) {
      status = 'Atenção';
      badgeClass = 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200';
    }
    
    return {
      name: unitName,
      time: timeStr,
      status,
      badgeClass
    };
  });
});

// Tab 3: Timeline & Traceability Search
import { watch } from 'vue';

const searchQuery = ref('');
const loadingTrace = ref(false);
const selectedTraceId = ref<number | null>(null);
const focusSuggestions = ref(false);

const searchSuggestions = computed(() => {
  if (!searchQuery.value.trim()) return [];
  const query = searchQuery.value.trim().toLowerCase();
  const queryClean = query.replace('#', '');
  return solicitacoes.value.filter(s => 
    s.nome_paciente.toLowerCase().includes(query) || 
    s.prontuario.toString().includes(query) ||
    (s.id && s.id.toString().includes(queryClean))
  ).slice(0, 5);
});

const selecionarSolicitacaoTrace = (s: SolicitacaoCobertura) => {
  if (s.id) {
    selectedTraceId.value = s.id;
    searchQuery.value = `#${s.id} - ${s.nome_paciente}`;
  }
  focusSuggestions.value = false;
};

// Auto-select first request as default trace
watch(solicitacoes, (newVal) => {
  if (newVal.length > 0 && selectedTraceId.value === null) {
    selectedTraceId.value = newVal[0].id || null;
  }
});

const traceSolicitacao = computed(() => {
  if (selectedTraceId.value !== null) {
    return solicitacoes.value.find(s => s.id === selectedTraceId.value) || null;
  }
  return filteredSolicitacoes.value[0] || null;
});



const traceSteps = computed(() => {
  if (!traceSolicitacao.value) return [];
  const sol = traceSolicitacao.value;
  const steps = [
    { date: new Date(sol.created_at || '').toLocaleString('pt-BR'), title: 'Solicitação criada', actor: `Solicitante: ${sol.solicitante}` }
  ];
  if (sol.data_auditoria) {
    steps.push({ date: new Date(sol.data_auditoria).toLocaleString('pt-BR'), title: `Solicitação ${sol.status}`, actor: `Auditor: ${sol.auditor_username || 'CCIRAS'}` });
  }
  if (sol.data_entrega) {
    steps.push({ date: new Date(sol.data_entrega).toLocaleString('pt-BR'), title: 'Liberada pela Farmácia', actor: `Farmacêutico: ${sol.farmaceutico_username || 'Farmácia'}` });
  }
  return steps;
});

const actionHistory = computed(() => {
  if (!traceSolicitacao.value) return [];
  const sol = traceSolicitacao.value;
  const history = [
    { 
      time: new Date(sol.created_at || '').toLocaleString('pt-BR'), 
      user: sol.solicitante, 
      sector: 'Enfermagem', 
      action: 'Solicitou', 
      actionBadge: 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-50 text-blue-700',
      note: 'Solicitação de curativo especial criada.'
    }
  ];
  if (sol.data_auditoria) {
    history.push({
      time: new Date(sol.data_auditoria).toLocaleString('pt-BR'),
      user: sol.auditor_username || 'CCIRAS',
      sector: 'CCIRAS',
      action: sol.status === 'NEGADO' ? 'Negou' : 'Autorizou',
      actionBadge: sol.status === 'NEGADO' ? 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-50 text-rose-700' : 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700',
      note: sol.justificativa || 'Parecer emitido.'
    });
  }
  if (sol.data_entrega) {
    history.push({
      time: new Date(sol.data_entrega).toLocaleString('pt-BR'),
      user: sol.farmaceutico_username || 'Farmácia',
      sector: 'Farmácia',
      action: 'Liberou',
      actionBadge: 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-700',
      note: sol.parecer_farmacia || 'Material entregue ao solicitante.'
    });
  }
  return history;
});

const showExportDropdown = ref(false);

const toggleExportDropdown = () => {
  showExportDropdown.value = !showExportDropdown.value;
};

const exportarCSV = () => {
  const data = filteredSolicitacoes.value;
  if (!data || data.length === 0) return;
  
  const headers = [
    'Data',
    'Paciente',
    'Prontuario',
    'Leito',
    'Solicitante',
    'Status',
    'Auditor',
    'Justificativa',
    'Farmaceutico',
    'Parecer Farmacia'
  ];
  
  const rows = data.map(s => [
    new Date(s.created_at || '').toLocaleDateString('pt-BR'),
    s.nome_paciente,
    s.prontuario,
    s.leito || '',
    s.solicitante,
    s.status || '',
    s.auditor_username || '',
    s.justificativa || '',
    s.farmaceutico_username || '',
    s.parecer_farmacia || ''
  ]);
  
  const csvContent = [
    headers.join(';'),
    ...rows.map(r => r.map(val => `"${String(val).replace(/"/g, '""')}"`).join(';'))
  ].join('\n');
  
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  link.setAttribute('href', url);
  link.setAttribute('download', `relatorio_solicitacoes_${new Date().toISOString().slice(0, 10)}.csv`);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const acaoExportar = (tipo: 'print' | 'csv' | 'pdf') => {
  showExportDropdown.value = false;
  if (tipo === 'print' || tipo === 'pdf') {
    window.print();
  } else if (tipo === 'csv') {
    exportarCSV();
  }
};
</script>

<style scoped>
@media print {
  .no-print {
    display: none !important;
  }
  
  /* Remove layout container padding, backgrounds, and shadows for printing */
  .space-y-6, .grid, .bg-white, .border {
    margin: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
    border: none !important;
    background-color: transparent !important;
  }
}
</style>
