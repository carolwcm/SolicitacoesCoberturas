<template>
  <div class="space-y-6">
    <!-- Header Area -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
      <div>
        <h1 class="text-2xl font-bold text-slate-800 tracking-tight">
          <span v-if="isCciras">Portal CCIRAS - Auditoria de Curativos</span>
          <span v-else-if="isFarmacia">Portal Farmácia - Liberação de Curativos</span>
          <span v-else>Portal Enfermagem - Acompanhamento de Pedidos</span>
        </h1>
        <p class="text-sm text-slate-500 mt-1">
          <span v-if="isCciras">Análise técnica, pareceres e autorização de coberturas especiais.</span>
          <span v-else-if="isFarmacia">Monitoramento de pareceres, controle de estoques e liberação final.</span>
          <span v-else>Acompanhe o status dos seus pedidos, pareceres técnicos e liberação de materiais.</span>
        </p>
      </div>

      <div class="flex items-center gap-3">
        <!-- CCIRAS manual import -->
        <Button v-if="isCciras" @click="importarDadosAghu" variant="primary" :loading="importing">
          <template #icon>
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H18.25" />
            </svg>
          </template>
          Atualizar
        </Button>

        <!-- Farmácia manual update -->
        <Button v-else-if="isFarmacia" @click="atualizarParecerCciras" variant="primary" :loading="loading">
          <template #icon>
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H18.25" />
            </svg>
          </template>
          Atualizar Parecer CCIRAS
        </Button>

        <!-- AGHU Simulation to ease testing -->
        <Button @click="showSimuladorModal = true" variant="default">
          Simular AGHU
        </Button>

        <ProfileDropdown />
      </div>
    </div>

    <!-- Admin View Toggle Selector -->
    <div v-if="authStore.isAdmin" class="flex justify-center bg-white p-2.5 rounded-2xl shadow-sm border border-slate-100 max-w-lg mx-auto">
      <div class="grid grid-cols-3 gap-2 w-full">
        <button 
          @click="modoExibicao = 'cciras'"
          :class="[
            modoExibicao === 'cciras' 
              ? 'bg-[#009688] text-white shadow-sm' 
              : 'bg-transparent text-slate-600 hover:bg-slate-50',
            'py-2 px-4 rounded-xl text-sm font-bold transition-all duration-200 cursor-pointer text-center'
          ]"
        >
          Visual CCIRAS
        </button>
        <button 
          @click="modoExibicao = 'farmacia'"
          :class="[
            modoExibicao === 'farmacia' 
              ? 'bg-[#009688] text-white shadow-sm' 
              : 'bg-transparent text-slate-600 hover:bg-slate-50',
            'py-2 px-4 rounded-xl text-sm font-bold transition-all duration-200 cursor-pointer text-center'
          ]"
        >
          Visual Farmácia
        </button>
        <button 
          @click="modoExibicao = 'enfermagem'"
          :class="[
            modoExibicao === 'enfermagem' 
              ? 'bg-[#009688] text-white shadow-sm' 
              : 'bg-transparent text-slate-600 hover:bg-slate-50',
            'py-2 px-4 rounded-xl text-sm font-bold transition-all duration-200 cursor-pointer text-center'
          ]"
        >
          Visual Enfermagem
        </button>
      </div>
    </div>

    <!-- METRICS CARDS SECTION -->
    <div :class="['grid gap-4', isFarmacia ? 'grid-cols-1 sm:grid-cols-3' : 'grid-cols-2 sm:grid-cols-4']">
      <div 
        v-for="card in metricCardsFiltrados" 
        :key="card.filterKey" 
        @click="selecionarFiltroCard(card.filterKey)"
        :class="[
          'p-5 rounded-2xl border shadow-sm flex flex-col justify-center items-center text-center hover:shadow-md transition-all duration-200 cursor-pointer select-none min-h-[130px]',
          filtroCardAtivo === card.filterKey 
            ? 'bg-indigo-50/70 border-indigo-300 ring-2 ring-indigo-500/20' 
            : 'bg-white border-slate-100'
        ]"
      >
        <span class="text-xs font-bold uppercase tracking-wider text-slate-500 block leading-tight">
          {{ card.label }}
          <span class="block mt-1">{{ card.sector }}</span>
        </span>
        <span class="text-3xl font-extrabold mt-2" :class="card.color">{{ card.value }}</span>
      </div>
    </div>

    <!-- FILTERS SECTION -->
    <div class="flex flex-col md:flex-row justify-between items-end gap-4 no-print mb-4 bg-white p-5 rounded-2xl border border-slate-100 shadow-sm animate-fade-in">
      <!-- Filtros da Esquerda (Unidade Funcional e Período) -->
      <div class="flex flex-wrap items-end gap-4 w-full md:w-auto">
        <!-- Filtro Unidade Funcional -->
        <div class="flex flex-col">
          <label class="text-xs font-bold text-slate-400 uppercase mb-1">Unidade Funcional</label>
          <select 
            v-model="filtroUnidade" 
            class="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm text-slate-700 font-semibold focus:outline-none focus:border-indigo-650 cursor-pointer min-w-[180px]"
          >
            <option value="">Todas</option>
            <option value="UTI Adulto">UTI Adulto</option>
            <option value="Clínica Médica">Clínica Médica</option>
            <option value="Clínica Cirúrgica">Clínica Cirúrgica</option>
            <option value="Emergência">Emergência</option>
            <option value="Ortopedia">Ortopedia</option>
            <option value="Pediatria">Pediatria</option>
            <option value="Oncologia">Oncologia</option>
          </select>
        </div>

        <!-- Filtro Período -->
        <div class="flex items-end gap-2 flex-wrap">
          <div class="flex flex-col">
            <label class="text-xs font-bold text-slate-400 uppercase mb-1">Período</label>
            <select 
              v-model="filtroPeriodo" 
              class="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm text-slate-700 font-semibold focus:outline-none focus:border-indigo-650 cursor-pointer min-w-[150px]"
            >
              <option value="todos">Todos</option>
              <option value="hoje">Hoje</option>
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
                v-model="filtroDataInicio" 
                type="date" 
                class="bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-sm text-slate-750 font-semibold focus:outline-none focus:border-indigo-650 cursor-pointer animate-fade-in"
              >
            </div>
            <div class="flex flex-col">
              <label class="text-xs font-bold text-slate-400 uppercase mb-1">Fim</label>
              <input 
                v-model="filtroDataFim" 
                type="date" 
                class="bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-sm text-slate-750 font-semibold focus:outline-none focus:border-indigo-650 cursor-pointer animate-fade-in"
              >
            </div>
          </div>
        </div>
      </div>

      <!-- Filtro da Direita (Nº da RM ou Nome do Paciente) -->
      <div class="w-full md:max-w-md">
        <label class="block text-sm font-bold text-slate-700 mb-2">Nº da RM ou Nome do Paciente</label>
        <div class="relative">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Ex: 1 ou João Silva"
            class="w-full border border-slate-200 rounded-xl py-2.5 pl-4 pr-10 text-sm focus:outline-none focus:border-indigo-600 bg-white"
          >
          <button class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <Card>
      <template #header>
        <div class="flex justify-between items-center">
          <h2 class="text-lg font-bold text-slate-700">Solicitações de Cobertura</h2>
          <span class="text-xs text-slate-400">Próxima sincronização automática em: {{ tempoParaSincronizar }} min</span>
        </div>
      </template>

      <div v-if="loading" class="py-12 flex justify-center">
        <LoadingIndicator />
      </div>
      <div v-else-if="solicitacoesFiltradas.length === 0" class="py-12 text-center text-slate-500 font-medium">
        Nenhuma solicitação encontrada no momento.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-100">
          <thead class="bg-slate-50">
            <!-- CCIRAS Headers -->
            <tr v-if="isCciras">
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Nº da RM</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Data</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Paciente</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Prontuário</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Unidade Solicitante</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Leito</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Itens Solicitados</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Situação CCIRAS</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Situação Farmácia</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Ações</th>
            </tr>
            <!-- Farmacia Headers -->
            <tr v-else>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Nº da RM</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Data</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Paciente</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Prontuário</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Unidade Solicitante</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Leito</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Situação CCIRAS</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Situação Farmácia</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-slate-100">
            <tr v-for="sol in solicitacoesFiltradas" :key="sol.id" class="hover:bg-slate-50/50 transition-colors duration-150">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600 font-bold">#{{ sol.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600 font-medium">{{ formatarData(sol.created_at) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-800">{{ sol.nome_paciente }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ sol.prontuario }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ sol.leito ? 'Ala Curativos' : 'Unidade Geral' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600 font-semibold">{{ sol.leito || 'N/A' }}</td>
              
              <!-- CCIRAS Item column -->
              <td v-if="isCciras" class="px-6 py-4 text-sm text-slate-600">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-55 text-indigo-700">
                  {{ sol.itens.length }} item(ns)
                </span>
              </td>

              <!-- Situação CCIRAS -->
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span :class="getStatusBadgeClass(getSituacaoCciras(sol))">
                  {{ getSituacaoCciras(sol) }}
                </span>
              </td>

              <!-- Situação Farmácia -->
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span :class="getStatusBadgeClass(getSituacaoFarmacia(sol))">
                  {{ getSituacaoFarmacia(sol) }}
                </span>
              </td>

              <!-- Actions column -->
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button @click="abrirAcoes(sol)" class="text-indigo-600 hover:text-indigo-900 bg-indigo-50 hover:bg-indigo-100 p-2 rounded-xl transition duration-150 inline-flex items-center cursor-pointer">
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>

    <!-- DETALHES MODAL (CCIRAS & FARMÁCIA) -->
    <Modal :show="showDetalhesModal" @close="showDetalhesModal = false" size="4xl">
      <template #header>
        Detalhes da Solicitação #{{ solicitacaoSelecionada?.id }}
      </template>

      <div class="space-y-6 py-2" v-if="solicitacaoSelecionada">
        <!-- Cabeçalho de Informações do Paciente -->
        <div class="grid grid-cols-2 gap-4 text-sm bg-slate-50 p-4 rounded-2xl border border-slate-100">
          <div><span class="font-semibold text-slate-500">Paciente:</span> {{ solicitacaoSelecionada.nome_paciente }}</div>
          <div><span class="font-semibold text-slate-500">Prontuário:</span> {{ solicitacaoSelecionada.prontuario }}</div>
          <div><span class="font-semibold text-slate-500">Unidade Solicitante:</span> {{ solicitacaoSelecionada.leito ? 'Ala Curativos' : 'Unidade Geral' }}</div>
          <div><span class="font-semibold text-slate-500">Leito:</span> {{ solicitacaoSelecionada.leito || 'N/A' }}</div>
          <div><span class="font-semibold text-slate-500">Data e Hora:</span> {{ formatarData(solicitacaoSelecionada.created_at) }}</div>
          <div><span class="font-semibold text-slate-500">Solicitante:</span> {{ solicitacaoSelecionada.solicitante }}</div>
        </div>

        <!-- Parecer CCIRAS anterior (exibido para a Farmácia) -->
        <div v-if="!isCciras && solicitacaoSelecionada.auditor_username" class="border border-indigo-100 bg-indigo-50/20 rounded-2xl p-4 space-y-2">
          <h3 class="font-bold text-indigo-950 text-sm">Parecer Anterior da CCIRAS</h3>
          <div class="grid grid-cols-2 gap-2 text-xs text-indigo-900">
            <div><span class="font-medium">Auditor:</span> {{ solicitacaoSelecionada.auditor_username }}</div>
            <div><span class="font-medium">Data:</span> {{ formatarData(solicitacaoSelecionada.data_auditoria) }}</div>
          </div>
          <p class="text-sm text-indigo-950 mt-2 italic">"{{ solicitacaoSelecionada.justificativa }}"</p>
        </div>

        <!-- LISTA DE ITENS PARA EDICAO -->
        <div>
          <h3 class="font-bold text-slate-800 mb-3">Coberturas e Quantidades</h3>
          <div class="space-y-3">
            <div v-for="item in (isCciras || isEnfermagem ? itensEdicao : itensEdicao.filter(i => i.status_item === 'AUTORIZADO' || i.status_item === 'AUDITADO' || i.status_item === 'NEGADO'))" :key="item.id" class="border border-slate-150 rounded-2xl p-4 bg-white flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div class="flex-1">
                <p class="font-semibold text-slate-900">{{ item.nome_material }}</p>
                <p class="text-xs text-slate-500">Código: {{ item.codigo_material }}</p>
              </div>

              <!-- Controle de Qtd para CCIRAS -->
              <div v-if="isCciras" class="flex items-center gap-2 md:gap-3">
                <div>
                  <span class="text-xs text-slate-400 block mb-1">Solicitada</span>
                  <span class="text-sm font-bold text-slate-800">{{ item.quantidade_solicitada }}</span>
                </div>
                <div>
                  <label class="block text-xs font-semibold text-slate-500 mb-1">Qtd Auditada</label>
                  <input type="number" v-model.number="item.quantidade_autorizada" min="0" :max="item.quantidade_solicitada" class="border rounded-xl p-1.5 w-20 text-center font-bold" @input="ajustarQuantidade(item)">
                </div>
                <button type="button" @click="marcarComoEmFalta(item)" class="self-end mb-0.5 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 px-3 py-2 rounded-xl text-xs font-bold transition duration-150 cursor-pointer">
                  Em falta
                </button>
                <button type="button" @click="negarItem(item)" class="self-end mb-0.5 bg-red-50 hover:bg-red-100 text-red-700 border border-red-200 px-3 py-2 rounded-xl text-xs font-bold transition duration-150 cursor-pointer">
                  Negar
                </button>
              </div>

              <!-- Controle de Qtd para Farmácia ou Enfermagem -->
              <div v-else class="flex items-center gap-4">
                <div>
                  <span class="text-xs text-slate-400 block mb-1">Auditada CCIRAS</span>
                  <span class="text-sm font-bold text-slate-800">{{ item.quantidade_autorizada }}</span>
                </div>
                
                <!-- Qtd Liberada (Editable for Farmácia, Read-only for Enfermagem) -->
                <div v-if="isFarmacia">
                  <label class="block text-xs font-semibold text-slate-500 mb-1">Qtd Liberada</label>
                  <input type="number" v-model.number="item.quantidade_liberada" min="0" :max="item.quantidade_autorizada" class="border rounded-xl p-1.5 w-24 text-center font-bold">
                </div>
                <div v-else>
                  <span class="text-xs text-slate-400 block mb-1">Qtd Liberada Farmácia</span>
                  <span class="text-sm font-bold text-slate-800">{{ item.quantidade_liberada !== null && item.quantidade_liberada !== undefined ? item.quantidade_liberada : 'Pendente' }}</span>
                </div>

                <button v-if="isFarmacia" type="button" @click="marcarComoEmFalta(item)" class="self-end mb-0.5 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 px-3 py-2 rounded-xl text-xs font-bold transition duration-150 cursor-pointer">
                  Em falta
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- PARECER TEXTAREA -->
        <div v-if="isCciras" class="form-group">
          <label class="block text-sm font-bold text-slate-700 mb-2">Parecer da CCIRAS</label>
          <textarea v-model="parecerCciras" rows="3" class="w-full border rounded-2xl p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none" placeholder="Digite a análise técnica e justificativa..."></textarea>
        </div>

        <div v-else-if="isFarmacia" class="form-group">
          <label class="block text-sm font-bold text-slate-700 mb-2">Parecer da Farmácia</label>
          <textarea v-model="parecerFarmacia" rows="3" class="w-full border rounded-2xl p-3 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none" placeholder="Digite a justificativa de entrega/liberação..."></textarea>
        </div>

        <!-- Enfermagem View Pareceres (Read-only status cards) -->
        <div v-else class="space-y-4">
          <div v-if="solicitacaoSelecionada.justificativa" class="border border-indigo-100 bg-indigo-50/20 rounded-2xl p-4 space-y-1">
            <h4 class="font-bold text-indigo-950 text-xs uppercase">Parecer CCIRAS (Auditoria)</h4>
            <div class="text-xs text-indigo-800">
              Auditor: {{ solicitacaoSelecionada.auditor_username || 'N/A' }} | Data: {{ formatarData(solicitacaoSelecionada.data_auditoria) }}
            </div>
            <p class="text-sm text-indigo-950 mt-1 italic">"{{ solicitacaoSelecionada.justificativa }}"</p>
          </div>
          <div v-else class="border border-slate-200 bg-slate-50/50 rounded-2xl p-4 text-xs font-semibold text-slate-500">
            Aguardando parecer da auditoria CCIRAS.
          </div>

          <div v-if="solicitacaoSelecionada.parecer_farmacia" class="border border-emerald-100 bg-emerald-50/20 rounded-2xl p-4 space-y-1">
            <h4 class="font-bold text-emerald-950 text-xs uppercase">Parecer Farmácia (Liberação)</h4>
            <div class="text-xs text-emerald-800">
              Farmacêutico: {{ solicitacaoSelecionada.farmaceutico_username || 'N/A' }} | Data: {{ formatarData(solicitacaoSelecionada.data_entrega) }}
            </div>
            <p class="text-sm text-emerald-950 mt-1 italic">"{{ solicitacaoSelecionada.parecer_farmacia }}"</p>
          </div>
          <div v-else-if="solicitacaoSelecionada.status === 'AUTORIZADO' || solicitacaoSelecionada.status === 'AUDITADO'" class="border border-slate-200 bg-slate-50/50 rounded-2xl p-4 text-xs font-semibold text-slate-500">
            Aguardando parecer e liberação da Farmácia.
          </div>
        </div>
      </div>

      <!-- DECISION BUTTONS -->
      <template #footer>
        <div class="flex flex-nowrap gap-1.5 justify-end w-full">
          <!-- CCIRAS Actions (3 buttons) -->
          <template v-if="isCciras">
            <Button @click="submeterDecisaoCciras('EM ANÁLISE')" class="!px-2.5 !py-1.5 !text-xs shrink-0" variant="default">Em Análise</Button>
            <Button @click="submeterDecisaoCciras('AUDITADO')" class="!px-2.5 !py-1.5 !text-xs shrink-0" variant="primary">Auditado</Button>
            <Button @click="submeterDecisaoCciras('LIBERADO')" class="!px-2.5 !py-1.5 !text-xs shrink-0" variant="success">Entregue CCIRAS</Button>
          </template>

          <!-- Farmácia Actions -->
          <template v-else-if="isFarmacia">
            <Button @click="submeterDecisaoFarmacia('LIBERADO')" variant="success">Liberado/Concluído</Button>
          </template>

          <!-- Enfermagem Actions -->
          <template v-else>
            <Button @click="showDetalhesModal = false" variant="default">Fechar</Button>
          </template>
        </div>
      </template>
    </Modal>

    <!-- SIMULADOR AGHU MODAL -->
    <Modal :show="showSimuladorModal" @close="showSimuladorModal = false">
      <template #header>Simulador de Entrada AGHU</template>
      <div class="space-y-4 py-2">
        <p class="text-sm text-slate-500">
          Simule o fluxo de um profissional solicitando coberturas especiais de curativos no sistema AGHU do hospital.
        </p>

        <div class="form-group">
          <label class="block text-xs font-semibold text-slate-600 mb-1">Paciente</label>
          <input type="text" v-model="simuladoPaciente" class="w-full border rounded-xl p-2.5 text-sm" placeholder="Nome Completo do Paciente">
        </div>

        <div class="form-group">
          <label class="block text-xs font-semibold text-slate-600 mb-1">Prontuário (Apenas números)</label>
          <input type="number" v-model.number="simuladoProntuario" class="w-full border rounded-xl p-2.5 text-sm" placeholder="Ex: 87462">
        </div>

        <div class="form-group">
          <label class="block text-xs font-semibold text-slate-600 mb-1">Leito</label>
          <input type="text" v-model="simuladoLeito" class="w-full border rounded-xl p-2.5 text-sm" placeholder="Ex: Leito 12 - UTI">
        </div>

        <div class="form-group">
          <label class="block text-xs font-semibold text-slate-600 mb-1">Solicitante</label>
          <input type="text" v-model="simuladoSolicitante" class="w-full border rounded-xl p-2.5 text-sm" placeholder="Ex: Enf. Mariana Souza">
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-2">Itens de Coberturas para Curativos</label>
          <div class="space-y-2 max-h-48 overflow-y-auto border rounded-xl p-3 bg-slate-50">
            <div v-for="item in coberturasPredefinidas" :key="item.codigo" class="flex items-center justify-between">
              <label class="flex items-center text-sm text-slate-700 cursor-pointer">
                <input type="checkbox" :value="item" v-model="simuladoItensSelecionados" class="rounded border-slate-300 text-indigo-600">
                <span class="ml-2 text-xs font-medium">{{ item.nome }}</span>
              </label>
              <div v-if="simuladoItensSelecionados.some(i => i.codigo === item.codigo)" class="flex items-center gap-2">
                <span class="text-xs text-slate-400">Qtd:</span>
                <input type="number" v-model.number="item.qtd" min="1" class="border rounded px-1.5 py-0.5 w-12 text-center text-xs">
              </div>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <Button @click="showSimuladorModal = false" variant="default">Cancelar</Button>
        <Button @click="enviarSimulacaoAghu" variant="primary">Criar Solicitação</Button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted, watch } from 'vue';
import { useToast } from 'vue-toastification';
import SolicitacoesService, { SolicitacaoCobertura } from '../services/SolicitacoesService';
import api from '../services/api';
import Card from '../components/Card.vue';
import Button from '../components/Button.vue';
import Modal from '../components/Modal.vue';
import LoadingIndicator from '../components/LoadingIndicator.vue';
import ProfileDropdown from '../components/ProfileDropdown.vue';
import { useAuthStore } from '../stores/auth';

const toast = useToast();
const authStore = useAuthStore();

// Perfil e Modo de Exibição
const modoExibicao = ref<'cciras' | 'farmacia' | 'enfermagem'>('cciras');

const isCciras = computed(() => {
  if (authStore.isAdmin) {
    return modoExibicao.value === 'cciras';
  }
  return authStore.isCciras;
});

const isFarmacia = computed(() => {
  if (authStore.isAdmin) {
    return modoExibicao.value === 'farmacia';
  }
  return authStore.isFarmacia;
});

const isEnfermagem = computed(() => {
  if (authStore.isAdmin) {
    return modoExibicao.value === 'enfermagem';
  }
  return !authStore.isCciras && !authStore.isFarmacia;
});

const loading = ref(false);
const importing = ref(false);
const solicitacoes = ref<SolicitacaoCobertura[]>([]);
const searchQuery = ref('');
const filtroUnidade = ref('');
const filtroPeriodo = ref('todos');
const filtroDataInicio = ref('');
const filtroDataFim = ref('');

// Modais
const showDetalhesModal = ref(false);
const showSimuladorModal = ref(false);
const solicitacaoSelecionada = ref<SolicitacaoCobertura | null>(null);

// Inputs para pareces e edições
const parecerCciras = ref('');
const parecerFarmacia = ref('');
const itensEdicao = ref<any[]>([]);

// Temporizadores para Sincronização Horária
const tempoParaSincronizar = ref(60);
let timerSincronizacao: any = null;

// Sincronização automática de hora em hora
const inicializarSincronizador = () => {
  timerSincronizacao = setInterval(() => {
    tempoParaSincronizar.value--;
    if (tempoParaSincronizar.value <= 0) {
      if (isCciras.value) {
        importarDadosAghu();
      } else {
        atualizarParecerCciras();
      }
      tempoParaSincronizar.value = 60;
    }
  }, 60000); // Executa a cada minuto
};

const getSituacaoCciras = (sol: SolicitacaoCobertura) => {
  if (sol.status && ['PENDENTE', 'EM ANÁLISE', 'NEGADO'].includes(sol.status)) {
    return sol.status;
  }
  return 'AUDITADO';
};

const getSituacaoFarmacia = (sol: SolicitacaoCobertura) => {
  if (sol.status && ['LIBERADO', 'ENTREGUE'].includes(sol.status)) {
    return 'LIBERADO/CONCLUÍDO';
  }
  if (sol.status === 'EM FALTA') {
    return 'EM FALTA';
  }
  if (sol.status === 'AUTORIZADO' || sol.status === 'AUDITADO') {
    return 'PENDENTE';
  }
  return 'PENDENTE';
};

// Métricas Dinâmicas
const pendentesCcirasCount = computed(() => solicitacoes.value.filter(s => s.status === 'PENDENTE').length);
const emAnaliseCcirasCount = computed(() => solicitacoes.value.filter(s => s.status === 'EM ANÁLISE').length);
const autorizadasCcirasCount = computed(() => solicitacoes.value.filter(s => s.status === 'AUTORIZADO' || s.status === 'AUDITADO').length);
const entregueCcirasCount = computed(() => solicitacoes.value.filter(s => ['LIBERADO', 'ENTREGUE'].includes(s.status || '')).length);

const pendentesFarmaciaCount = computed(() => solicitacoes.value.filter(s => s.status === 'AUTORIZADO' || s.status === 'AUDITADO').length);
const autorizadasFarmaciaCount = computed(() => solicitacoes.value.filter(s => ['LIBERADO', 'ENTREGUE'].includes(s.status || '')).length);
const entregueFarmaciaCount = computed(() => solicitacoes.value.filter(s => ['LIBERADO', 'ENTREGUE'].includes(s.status || '')).length);

const metricCardsFiltrados = computed(() => {
  if (isCciras.value) {
    return [
      { label: 'PENDENTES', sector: 'CCIRAS', value: pendentesCcirasCount.value, color: 'text-yellow-600', filterKey: 'PENDENTES - CCIRAS' },
      { label: 'EM ANÁLISE', sector: 'CCIRAS', value: emAnaliseCcirasCount.value, color: 'text-orange-550', filterKey: 'EM ANÁLISE - CCIRAS' },
      { label: 'AUDITADAS', sector: 'CCIRAS', value: autorizadasCcirasCount.value, color: 'text-blue-600', filterKey: 'AUDITADAS - CCIRAS' },
      { label: 'ENTREGUE', sector: 'CCIRAS', value: entregueCcirasCount.value, color: 'text-emerald-600', filterKey: 'ENTREGUE - CCIRAS' }
    ];
  } else if (isFarmacia.value) {
    return [
      { label: 'PENDENTES', sector: 'FARMÁCIA', value: pendentesFarmaciaCount.value, color: 'text-yellow-600', filterKey: 'PENDENTES - FARMÁCIA' },
      { label: 'AVALIADAS', sector: 'FARMÁCIA', value: autorizadasFarmaciaCount.value, color: 'text-blue-600', filterKey: 'AVALIADAS - FARMÁCIA' },
      { label: 'ENTREGUE', sector: 'FARMÁCIA', value: entregueFarmaciaCount.value, color: 'text-emerald-600', filterKey: 'ENTREGUE - FARMÁCIA' }
    ];
  } else {
    const mySols = solicitacoes.value.filter(s => s.solicitante === authStore.user?.username);
    const pendentes = mySols.filter(s => s.status === 'PENDENTE').length;
    const emAnalise = mySols.filter(s => s.status === 'EM ANÁLISE').length;
    const auditadas = mySols.filter(s => s.status === 'AUTORIZADO' || s.status === 'AUDITADO').length;
    const entregues = mySols.filter(s => ['LIBERADO', 'ENTREGUE'].includes(s.status || '')).length;
    
    return [
      { label: 'PENDENTES', sector: 'ENFERMAGEM', value: pendentes, color: 'text-yellow-600', filterKey: 'PENDENTES - ENFERMAGEM' },
      { label: 'EM ANÁLISE', sector: 'ENFERMAGEM', value: emAnalise, color: 'text-orange-550', filterKey: 'EM ANÁLISE - ENFERMAGEM' },
      { label: 'AUDITADAS', sector: 'ENFERMAGEM', value: auditadas, color: 'text-blue-600', filterKey: 'AUDITADAS - ENFERMAGEM' },
      { label: 'ENTREGUES', sector: 'ENFERMAGEM', value: entregues, color: 'text-emerald-600', filterKey: 'ENTREGUES - ENFERMAGEM' }
    ];
  }
});

const filtroCardAtivo = ref<string | null>(null);

const selecionarFiltroCard = (title: string) => {
  if (filtroCardAtivo.value === title) {
    filtroCardAtivo.value = null;
  } else {
    filtroCardAtivo.value = title;
  }
};

watch(isCciras, () => {
  filtroCardAtivo.value = null;
});

const solicitacoesFiltradas = computed(() => {
  let list = solicitacoes.value;

  // Filtro específico do perfil de Enfermagem (ver apenas seus próprios pedidos)
  if (isEnfermagem.value && authStore.user?.givenName?.[0]) {
    // Tenta casar pelo solicitante
    const usernameLogado = authStore.user.username.toLowerCase();
    const nomeLogado = authStore.user.givenName[0].toLowerCase();
    list = list.filter(s => {
      const solLower = s.solicitante.toLowerCase();
      return solLower.includes(usernameLogado) || solLower.includes(nomeLogado);
    });
  }

  // Filtro por Unidade Funcional
  if (filtroUnidade.value) {
    list = list.filter(s => {
      if (!s.leito) return false;
      return s.leito.toLowerCase().includes(filtroUnidade.value.toLowerCase());
    });
  }

  // Filtro por Período
  if (filtroPeriodo.value !== 'todos') {
    const now = new Date();
    list = list.filter(s => {
      if (!s.created_at) return false;
      const date = new Date(s.created_at);
      if (filtroPeriodo.value === 'hoje') {
        return date.getDate() === now.getDate() && date.getMonth() === now.getMonth() && date.getFullYear() === now.getFullYear();
      }
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
        if (filtroDataInicio.value) {
          const start = new Date(filtroDataInicio.value + 'T00:00:00');
          if (date < start) return false;
        }
        if (filtroDataFim.value) {
          const end = new Date(filtroDataFim.value + 'T23:59:59');
          if (date > end) return false;
        }
        return true;
      }
      return true;
    });
  }

  if (filtroCardAtivo.value) {
    const cardTitle = filtroCardAtivo.value;
    if (cardTitle === 'PENDENTES - CCIRAS') {
      list = list.filter(s => s.status === 'PENDENTE');
    } else if (cardTitle === 'EM ANÁLISE - CCIRAS') {
      list = list.filter(s => s.status === 'EM ANÁLISE');
    } else if (cardTitle === 'AUDITADAS - CCIRAS') {
      list = list.filter(s => s.status === 'AUTORIZADO' || s.status === 'AUDITADO');
    } else if (cardTitle === 'ENTREGUE - CCIRAS') {
      list = list.filter(s => ['LIBERADO', 'ENTREGUE'].includes(s.status || ''));
    } else if (cardTitle === 'PENDENTES - FARMÁCIA') {
      list = list.filter(s => s.status === 'AUTORIZADO' || s.status === 'AUDITADO');
    } else if (cardTitle === 'AVALIADAS - FARMÁCIA') {
      list = list.filter(s => ['LIBERADO', 'ENTREGUE'].includes(s.status || ''));
    } else if (cardTitle === 'ENTREGUE - FARMÁCIA') {
      list = list.filter(s => ['LIBERADO', 'ENTREGUE'].includes(s.status || ''));
    } else if (cardTitle === 'PENDENTES - ENFERMAGEM') {
      list = list.filter(s => s.status === 'PENDENTE');
    } else if (cardTitle === 'EM ANÁLISE - ENFERMAGEM') {
      list = list.filter(s => s.status === 'EM ANÁLISE');
    } else if (cardTitle === 'AUDITADAS - ENFERMAGEM') {
      list = list.filter(s => s.status === 'AUTORIZADO' || s.status === 'AUDITADO');
    } else if (cardTitle === 'ENTREGUES - ENFERMAGEM') {
      list = list.filter(s => ['LIBERADO', 'ENTREGUE'].includes(s.status || ''));
    }
  }
  
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.trim().toLowerCase();
    const queryClean = query.replace('#', '');
    list = list.filter(s => 
      s.nome_paciente.toLowerCase().includes(query) || 
      s.prontuario.toString().includes(query) ||
      (s.id && s.id.toString() === queryClean) ||
      (s.id && s.id.toString().includes(queryClean))
    );
  }
  
  return list;
});

const formatarData = (dataStr?: string | null) => {
  if (!dataStr) return 'N/A';
  return new Date(dataStr).toLocaleString('pt-BR');
};

const getStatusBadgeClass = (status?: string) => {
  switch (status?.toUpperCase()) {
    case 'PENDENTE':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-yellow-50 text-yellow-700 border border-yellow-200';
    case 'EM ANÁLISE':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-orange-50 text-orange-700 border border-orange-200';
    case 'AUTORIZADO':
    case 'AUDITADO':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-blue-50 text-blue-700 border border-blue-200';
    case 'NEGADO':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200';
    case 'LIBERADO':
    case 'LIBERADO/CONCLUÍDO':
    case 'ENTREGUE':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
    case 'EM FALTA':
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-slate-100 text-slate-700 border border-slate-350';
    default:
      return 'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-50 text-slate-600';
  }
};

const carregarSolicitacoes = async () => {
  loading.value = true;
  try {
    solicitacoes.value = await SolicitacoesService.listar();
  } catch (err) {
    toast.error('Falha ao carregar as solicitações.');
  } finally {
    loading.value = false;
  }
};

const importarDadosAghu = async () => {
  importing.value = true;
  try {
    await api.post('/api/solicitacoes/importar');
    toast.success('Dados importados com sucesso do AGHU!');
    await carregarSolicitacoes();
  } catch (e) {
    toast.error('Erro ao conectar e importar dados do AGHU.');
  } finally {
    importing.value = false;
  }
};

const atualizarParecerCciras = async () => {
  await carregarSolicitacoes();
  toast.success('Pareceres da CCIRAS atualizados!');
};

// Ações ao clicar na tabela
const abrirAcoes = (sol: SolicitacaoCobertura) => {
  solicitacaoSelecionada.value = sol;
  parecerCciras.value = sol.justificativa || '';
  parecerFarmacia.value = sol.parecer_farmacia || '';
  itensEdicao.value = sol.itens.map(i => {
    const qtdAut = i.quantidade_autorizada !== null && i.quantidade_autorizada !== undefined ? i.quantidade_autorizada : i.quantidade_solicitada;
    const qtdLib = i.quantidade_liberada !== null && i.quantidade_liberada !== undefined ? i.quantidade_liberada : qtdAut;
    return {
      ...i,
      quantidade_autorizada: qtdAut,
      quantidade_liberada: qtdLib
    };
  });
  showDetalhesModal.value = true;
};

// CCIRAS Decision Submission
const submeterDecisaoCciras = async (statusGeral: string) => {
  if (!solicitacaoSelecionada.value?.id) return;

  let statusParaEnviar = statusGeral;
  if (statusGeral === 'AUDITADO') {
    const todosNegados = itensEdicao.value.every(i => i.quantidade_autorizada === 0 || i.status_item === 'NEGADO');
    if (todosNegados) {
      statusParaEnviar = 'NEGADO';
    }
  }

  const originalItens = solicitacaoSelecionada.value.itens || [];
  const alterouQuantidade = itensEdicao.value.some(item => {
    const originalItem = originalItens.find(o => o.id === item.id);
    const originalQtd = originalItem 
      ? (originalItem.quantidade_autorizada !== null && originalItem.quantidade_autorizada !== undefined ? originalItem.quantidade_autorizada : originalItem.quantidade_solicitada)
      : item.quantidade_solicitada;
    return item.quantidade_autorizada !== originalQtd;
  });

  const temNegado = itensEdicao.value.some(i => i.quantidade_autorizada === 0 || i.status_item === 'NEGADO');
  const precisaParecer = statusParaEnviar === 'NEGADO' || statusParaEnviar === 'EM ANÁLISE' || alterouQuantidade || temNegado;

  if (precisaParecer && !parecerCciras.value.trim()) {
    toast.warning('Por favor, registre a justificativa técnica/parecer da CCIRAS.');
    return;
  }

  try {
    const payload = {
      status_geral: statusParaEnviar,
      justificativa: parecerCciras.value,
      itens: itensEdicao.value.map(i => {
        let itemStatus = 'AUDITADO';
        if (i.quantidade_autorizada === 0 || i.status_item === 'NEGADO') {
          itemStatus = 'NEGADO';
        }
        return {
          id: i.id!,
          quantidade_autorizada: i.quantidade_autorizada,
          status_item: itemStatus
        };
      })
    };
    await SolicitacoesService.auditar(solicitacaoSelecionada.value.id, payload);
    
    if (statusParaEnviar === 'LIBERADO') {
      toast.success('Entregue - Egresso registrado com sucesso!');
    } else if (statusParaEnviar === 'AUDITADO') {
      toast.success('Auditado com sucesso');
    } else if (statusParaEnviar === 'NEGADO') {
      toast.success('solicitação negada com sucesso');
    } else {
      toast.success('Parecer da CCIRAS enviado com sucesso!');
    }
    
    showDetalhesModal.value = false;
    await carregarSolicitacoes();
  } catch (e) {
    toast.error('Falha ao registrar a auditoria da CCIRAS.');
  }
};

// Farmácia Decision Submission
const submeterDecisaoFarmacia = async (statusGeral: string) => {
  if (!solicitacaoSelecionada.value?.id) return;

  const situacaoCciras = getSituacaoCciras(solicitacaoSelecionada.value);
  if (situacaoCciras === 'PENDENTE' || situacaoCciras === 'EM ANÁLISE') {
    toast.warning('Auditoria da CCIRAS PENDENTE. Aguarde auditoria.');
    return;
  }

  const alterouParaValorMaiorQueZero = itensEdicao.value.some(i => i.quantidade_liberada !== i.quantidade_autorizada && i.quantidade_liberada > 0);
  if (alterouParaValorMaiorQueZero && !parecerFarmacia.value.trim()) {
    toast.warning('Por favor, registre a justificativa/parecer da Farmácia.');
    return;
  }

  // Se todos os itens autorizados estão com quantidade_liberada = 0, o status geral deve ser 'EM FALTA'
  const itensAutorizados = itensEdicao.value.filter(i => i.status_item === 'AUTORIZADO' || i.status_item === 'AUDITADO');
  const todosEmFalta = itensAutorizados.length > 0 && itensAutorizados.every(i => i.quantidade_liberada === 0);
  const statusParaEnviar = todosEmFalta ? 'EM FALTA' : statusGeral;

  try {
    const payload = {
      status_geral: statusParaEnviar,
      justificativa: parecerFarmacia.value,
      itens: itensEdicao.value.map(i => ({
        id: i.id!,
        quantidade_liberada: i.quantidade_liberada
      }))
    };
    await SolicitacoesService.entregar(solicitacaoSelecionada.value.id, payload);
    toast.success('Decisão da Farmácia registrada!');
    showDetalhesModal.value = false;
    await carregarSolicitacoes();
  } catch (e) {
    toast.error('Falha ao registrar a liberação da Farmácia.');
  }
};

const marcarComoEmFalta = (item: any) => {
  if (isCciras.value) {
    item.quantidade_autorizada = 0;
    const msg = `${item.nome_material} em falta`;
    if (!parecerCciras.value.trim()) {
      parecerCciras.value = msg;
    } else if (!parecerCciras.value.includes(msg)) {
      parecerCciras.value += `\n${msg}`;
    }
  } else {
    item.quantidade_liberada = 0;
    const msg = `${item.nome_material} em falta`;
    if (!parecerFarmacia.value.trim()) {
      parecerFarmacia.value = msg;
    } else if (!parecerFarmacia.value.includes(msg)) {
      parecerFarmacia.value += `\n${msg}`;
    }
  }
};

const negarItem = (item: any) => {
  item.quantidade_autorizada = 0;
  item.status_item = 'NEGADO';
  const msg = `${item.nome_material} negado`;
  if (!parecerCciras.value.trim()) {
    parecerCciras.value = msg;
  } else if (!parecerCciras.value.includes(msg)) {
    parecerCciras.value += `\n${msg}`;
  }
};

const ajustarQuantidade = (item: any) => {
  if (item.quantidade_autorizada > 0) {
    item.status_item = 'AUDITADO';
  }
};

// AGHU SIMULATION FIELDS
const simuladoPaciente = ref('Ana Maria Custódio');
const simuladoProntuario = ref(384729);
const simuladoLeito = ref('Leito 104 - Enfermaria');
const simuladoSolicitante = ref('Dr. Juliano Bastos');
const simuladoItensSelecionados = ref<any[]>([]);

const coberturasPredefinidas = ref([
  { codigo: 10401, nome: 'Curativo Hidrocolóide Extra Fino 10x10', qtd: 5 },
  { codigo: 10402, nome: 'Curativo com Prata Nanocristalina 10x12', qtd: 2 },
  { codigo: 10403, nome: 'Espuma de Poliuretano com Silicone', qtd: 4 },
  { codigo: 10404, nome: 'Alginato de Cálcio e Sódio', qtd: 3 }
]);

const enviarSimulacaoAghu = async () => {
  if (!simuladoPaciente.value || !simuladoProntuario.value || simuladoItensSelecionados.value.length === 0) {
    toast.warning('Preencha os campos obrigatórios e escolha coberturas.');
    return;
  }

  try {
    const payload: SolicitacaoCobertura = {
      prontuario: simuladoProntuario.value,
      nome_paciente: simuladoPaciente.value,
      leito: simuladoLeito.value,
      solicitante: simuladoSolicitante.value,
      itens: simuladoItensSelecionados.value.map(i => ({
        codigo_material: i.codigo,
        nome_material: i.nome,
        quantidade_solicitada: i.qtd
      }))
    };
    await SolicitacoesService.criarMock(payload);
    toast.success('Solicitação simulada criada!');
    showSimuladorModal.value = false;
    await carregarSolicitacoes();
  } catch (e) {
    toast.error('Erro ao simular solicitação.');
  }
};

onMounted(() => {
  carregarSolicitacoes();
  inicializarSincronizador();
  
  // Define o modo inicial
  if (authStore.isAdmin) {
    modoExibicao.value = 'cciras';
  } else if (authStore.isCciras) {
    modoExibicao.value = 'cciras';
  } else if (authStore.isFarmacia) {
    modoExibicao.value = 'farmacia';
  } else {
    modoExibicao.value = 'enfermagem';
  }
});

onUnmounted(() => {
  if (timerSincronizacao) {
    clearInterval(timerSincronizacao);
  }
});
</script>
