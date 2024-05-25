url = "https://s2gpr.sefaz.ce.gov.br/fornecedor-web/paginas/cadastro_pessoas_compras/AssistenteEmissaoCRC.seam"
comp_doc_table = "//table[@id='formularioDeBusca:tableDocComplementarPessoaJuridica']"

comp_doc_table_subheader = f"{comp_doc_table}//thead"

comp_doc_table_body = f"{comp_doc_table}//tbody[@id='formularioDeBusca:tableDocComplementarPessoaJuridica:tb']"
consult_button = "//input[@id='formularioDeBusca:pesquisar']"
cnpj_input = "//input[@id='formularioDeBusca:filtroCnpjDecorate:filtroCnpj']"
juridic_person_button = "//input[@id='formularioDeBusca:j_id111:j_id123:1']"
table_items = [["STATUS"], ["NÚMERO"], ["COMPLEMENTO"], ["TIPO"], ["EMISSÃO"], ["VALIDADE"], ["EMISSOR"]]
