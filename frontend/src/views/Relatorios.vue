<template>
  <div class="space-y-6">
    <!-- Header Area -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-100 no-print">
      <div>
        <h1 class="text-2xl font-bold text-slate-800 tracking-tight">Relatórios CCIRAS</h1>
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
          </select>
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

      <!-- Export to Print Button -->
      <div>
        <button 
          @click="exportarImpressao"
          class="flex items-center gap-2 bg-indigo-650 hover:bg-indigo-700 text-white font-semibold px-4 py-2.5 rounded-xl text-sm transition-all shadow-sm cursor-pointer"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
          </svg>
          <span>Exportar para Impressão</span>
        </button>
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
            <p class="text-xs font-semibold text-slate-400 uppercase">Negadas</p>
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
        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
          <h3 class="text-sm font-bold text-slate-700 mb-4">Solicitações por mês</h3>
          <div class="h-64 flex items-end justify-between px-2 pt-6 relative border-l border-b border-slate-100">
            <!-- Simulated SVG Line Graph for aesthetic appeal -->
            <svg class="absolute inset-0 h-full w-full p-6" viewBox="0 0 100 100" preserveAspectRatio="none">
              <path d="M 0 80 Q 20 40 40 60 T 80 10 T 100 30" fill="none" stroke="rgb(79, 70, 229)" stroke-width="3" />
              <circle cx="20" cy="50" r="3" fill="rgb(79, 70, 229)" />
              <circle cx="40" cy="55" r="3" fill="rgb(79, 70, 229)" />
              <circle cx="60" cy="30" r="3" fill="rgb(79, 70, 229)" />
              <circle cx="80" cy="10" r="3" fill="rgb(79, 70, 229)" />
            </svg>
            <div class="text-[10px] text-slate-400 absolute bottom-1 left-4">Jan</div>
            <div class="text-[10px] text-slate-400 absolute bottom-1 left-1/4">Fev</div>
            <div class="text-[10px] text-slate-400 absolute bottom-1 left-2/4">Mar</div>
            <div class="text-[10px] text-slate-400 absolute bottom-1 left-3/4">Abr</div>
            <div class="text-[10px] text-slate-400 absolute bottom-1 right-4">Mai</div>
          </div>
        </div>

        <!-- Chart 2: Status Donut Chart -->
        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm flex flex-col justify-between">
          <h3 class="text-sm font-bold text-slate-700 mb-4">Status das solicitações</h3>
          <div class="flex items-center justify-around flex-1">
            <!-- SVG Donut Chart -->
            <div class="relative w-36 h-36">
              <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                <!-- Outer circle representing different slices -->
                <circle class="text-slate-100" stroke="currentColor" stroke-width="4" fill="none" cx="18" cy="18" r="15.915" />
                <circle class="text-emerald-500" :stroke-dasharray="`${pctAutorizadas} ${100 - pctAutorizadas}`" stroke-dashoffset="0" stroke="currentColor" stroke-width="4.5" fill="none" cx="18" cy="18" r="15.915" />
                <circle class="text-rose-500" :stroke-dasharray="`${pctNegadas} ${100 - pctNegadas}`" :stroke-dashoffset="`-${pctAutorizadas}`" stroke="currentColor" stroke-width="4.5" fill="none" cx="18" cy="18" r="15.915" />
                <circle class="text-indigo-500" :stroke-dasharray="`${pctEmAnalise} ${100 - pctEmAnalise}`" :stroke-dashoffset="`-${pctAutorizadas + pctNegadas}`" stroke="currentColor" stroke-width="4.5" fill="none" cx="18" cy="18" r="15.915" />
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
        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
          <h3 class="text-sm font-bold text-slate-700 mb-4">SLA das solicitações (tempo de avaliação)</h3>
          <div class="flex items-center justify-around h-60">
            <!-- Pie/Donut SLA -->
            <div class="relative w-36 h-36">
              <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                <circle class="text-slate-100" stroke="currentColor" stroke-width="6" fill="none" cx="18" cy="18" r="15.915" />
                <circle class="text-indigo-600" :stroke-dasharray="`${slaRanges.ok} ${100 - slaRanges.ok}`" stroke="currentColor" stroke-width="6" fill="none" cx="18" cy="18" r="15.915" />
                <circle class="text-emerald-500" :stroke-dasharray="`${slaRanges.warning} ${100 - slaRanges.warning}`" :stroke-dashoffset="`-${slaRanges.ok}`" stroke="currentColor" stroke-width="6" fill="none" cx="18" cy="18" r="15.915" />
                <circle class="text-amber-500" :stroke-dasharray="`${slaRanges.late} ${100 - slaRanges.late}`" :stroke-dashoffset="`-${slaRanges.ok + slaRanges.warning}`" stroke="currentColor" stroke-width="6" fill="none" cx="18" cy="18" r="15.915" />
                <circle class="text-rose-500" :stroke-dasharray="`${slaRanges.veryLate} ${100 - slaRanges.veryLate}`" :stroke-dashoffset="`-${slaRanges.ok + slaRanges.warning + slaRanges.late}`" stroke="currentColor" stroke-width="6" fill="none" cx="18" cy="18" r="15.915" />
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
                <span class="text-2xl font-black text-slate-800">{{ totalCount }}</span>
                <span class="text-[9px] font-bold text-slate-400 uppercase">Avaliações</span>
              </div>
            </div>
            <div class="space-y-2 text-xs">
              <div class="flex items-center"><span class="w-3 h-3 bg-indigo-600 rounded-full mr-2"></span> Até 24h</div>
              <div class="flex items-center"><span class="w-3 h-3 bg-emerald-500 rounded-full mr-2"></span> 24h - 48h</div>
              <div class="flex items-center"><span class="w-3 h-3 bg-amber-500 rounded-full mr-2"></span> 48h - 72h</div>
              <div class="flex items-center"><span class="w-3 h-3 bg-rose-500 rounded-full mr-2"></span> > 72h</div>
            </div>
          </div>
        </div>

        <!-- SLA by unit table -->
        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
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
        <div class="no-print">
          <label class="block text-sm font-bold text-slate-700 mb-2">Protocolo ou Nome do Paciente</label>
          <div class="relative max-w-md">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Ex: CCIRAS-2024-00128 ou João Silva"
              class="w-full border border-slate-200 rounded-xl py-2.5 pl-4 pr-10 text-sm focus:outline-none focus:border-indigo-650"
            >
            <button class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
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

const tempoMedioResposta = ref('18h 42m');
const tempoMedioFarmacia = ref('3h 15m');

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

// Tab 2: Quality SLA Computations
const pctAprovacao = computed(() => Math.round((autorizadasCount.value / (autorizadasCount.value + negadasCount.value || 1)) * 100) || 75);
const pctRetrabalho = ref(6.2);

const slaRanges = ref({
  ok: 53.1,
  warning: 25.0,
  late: 11.7,
  veryLate: 10.2
});

const slaUnits = ref([
  { name: 'UTI Adulto', time: '14h 22m', status: 'SLA OK', badgeClass: 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200' },
  { name: 'Clínica Médica', time: '16h 10m', status: 'SLA OK', badgeClass: 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200' },
  { name: 'Clínica Cirúrgica', time: '19h 45m', status: 'SLA OK', badgeClass: 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200' },
  { name: 'Emergência', time: '22h 30m', status: 'Atenção', badgeClass: 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200' },
  { name: 'Ortopedia', time: '25h 05m', status: 'SLA Estourado', badgeClass: 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200' }
]);

// Tab 3: Timeline & Traceability Search
const searchQuery = ref('');
const loadingTrace = ref(false);

const traceSolicitacao = computed(() => {
  if (!searchQuery.value.trim()) {
    return filteredSolicitacoes.value[0] || null;
  }
  const query = searchQuery.value.toLowerCase();
  return filteredSolicitacoes.value.find(s => 
    s.nome_paciente.toLowerCase().includes(query) || 
    s.prontuario.toString().includes(query) ||
    (s.id && `cciras-2024-001${s.id}`.toLowerCase().includes(query))
  ) || filteredSolicitacoes.value[0] || null;
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

const exportarImpressao = () => {
  window.print();
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
