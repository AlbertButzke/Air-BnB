Optar por classificação, uma quebra mais inteligente e alinhada ao negócio seria baseada nos quartis/percentis ou no comportamento do usuário, por exemplo:
 + Classe 1: < 4.0 (Acomodações ruins / Críticas)
 + Classe 2: 4.0 - 4.5 (Acomodações medianas, com problemas pontuais)
 + Classe 3: 4.5 - 4.75 (Acomodações boas)
 + Classe 4: 4.75 - 4.9 (Acomodações muito boas / Superhosts frequentes)
 + Classe 5: 4.9 - 5.0 (Acomodações excepcionais)

Recomendações:
Em vez de escolher um ou outro puramente, a melhor prática para dados do Airbnb costuma ser:
- Regressão com algoritmo robusto a outliers/assimetria: Use modelos de árvore como XGBoost, LightGBM ou CatBoost configurados para regressão. Eles lidam muito bem com essa assimetria de notas altas sem precisar categorizar os dados.
- Métrica de Avaliação Certa: Não use apenas o MSE (Mean Squared Error), pois ele penaliza demais erros grandes em notas baixas raras. Monitore o MAE (Mean Absolute Error).
- Abordagem Ordinal (Se quiser classificar): Se for mesmo usar intervalos, utilize Classificação Ordinal (onde o modelo sabe que a classe 4 está mais perto da 5 do que da 1), e não multiclass pura.