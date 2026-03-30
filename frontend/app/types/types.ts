// --- AUTH & USER ---
export type PerfilTipo = 'Gestor' | 'Financeiro' | 'Disciplinar' | 'Suporte' | 'Estudante' | 'Encarregado';

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  perfil: number;
  perfil_nome: PerfilTipo;
  precisa_mudar_senha: boolean;
}

// --- NÚCLEO (BUSINESS MODELS) ---

export interface Estudante {
  utilizador_id: number;
  nome_completo: string;
  num_estudante: string;
  email: string;
  genero: 'M' | 'F';
  curso: string;
  estado: 'Activo' | 'Inactivo' | 'Suspenso' | 'Graduado';
  quarto?: number | Quarto;
  quarto_numero?: string;
  encarregado?: number;
}

export interface Encarregado {
  utilizador_id: number;
  nome_completo: string;
  telefone_principal: string;
  email_contacto: string;
  educandos?: string[]; // No teu serializer é um StringRelatedField
}

export interface Quarto {
  id: number;
  numero: string;
  bloco: string;
  capacidade_maxima: number;
  genero_permitido: 'M' | 'F' | 'Misto';
  estado: 'Activo' | 'Manutenção' | 'Interditado';
  ocupacao_atual: number;
  vagas_disponiveis: number;
}

// --- FINANCEIRO & DISCIPLINAR ---

export interface Mensalidade {
  id: number;
  estudante_nome: string;
  mes_referencia: string; // ISO Date ou string formatada
  ano_referencia: number;
  valor: number;
  estado: 'Pendente' | 'Pago' | 'Atraso';
  data_pagamento?: string;
  metodo_pagamento?: 'M-Pesa' | 'e-Mola' | 'Transferência' | 'Numerário';
  numero_recibo?: string;
}

export interface Sancao {
  id: number;
  estudante_nome: string;
  tipo_sancao: string;
  data_ocorrencia: string;
  descricao: string;
  gravidade: 'Leve' | 'Media' | 'Grave';
}

export interface PedidoSaida {
  id: number;
  estudante_nome: string;
  data_submissao: string;
  data_saida_pretendida: string;
  data_retorno_pretendida: string;
  motivo: string;
  estado: 'Pendente' | 'Aguardando_Encarregado' | 'Autorizado' | 'Rejeitado';
  observacao_admin?: string;
}

// --- DASHBOARD (O PAYLOAD DO TEU ADMIN VIEW) ---

export interface DashboardResponse {
  administrative?: {
    total_estudantes_ativos: number;
    total_pedidos_pendentes: number;
    ocupacao_total: number;
  };
  finance?: {
    receita_mes_total: number;
    pagamentos_pendentes: number;
    taxa_inadimplencia: number;
  };
  discipline?: {
    total_sancoes_mes: number;
    top_infratores: Array<{ nome: string; total: number }>;
    top_ausentes: Array<{ nome: string; total: number }>;
  };
}

// --- UTILITÁRIOS (CHOICES DA OPCOESVIEW) ---

export interface OptionItem {
  value: string | number;
  label: string;
}

export interface AppOptions {
  perfis: OptionItem[];
  estudante_estados: OptionItem[];
  mensalidade_metodos: OptionItem[];
  mensalidade_estados: OptionItem[];
  presenca_estados: OptionItem[];
  sancao_tipos: OptionItem[];
  pedido_saida_estados: OptionItem[];
  quarto_estados: OptionItem[];
}