from functions import *
import streamlit as st
import datetime
import warnings
import altair as alt
import plotly.express as px
import functions

warnings.filterwarnings("ignore")

st.set_page_config(page_title="WhatsApp Group Chat Analysis")

selected_language = st.sidebar.selectbox('Select the Language / Dil Seçiniz', ('English', 'Türkçe'))

tabs = ["How to Use / Nasıl Kullanılır", "Model Application / Örnek Uygulama", "Do Your Own Analysis / Kendi Analizinizi Yapın"]

page = st.sidebar.radio("Tabs / Sayfalar", tabs)


if selected_language == "English":

    if page == "How to Use / Nasıl Kullanılır":
        st.markdown("<h1 style='text-align:center;'>WhatsApp Group Chat Analysis</h1>",unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>How to Use</h2>", unsafe_allow_html=True)
        st.write("""This project is an application that analyzes whatsapp group chats, visualizes basic statistical information and presents it to the user.""")
        st.write("""You can review the sample project in the Model Application section and make your own analysis in the Do Your Own Analysis section.""")
        st.write("""But first, don't forget to thoroughly read How To Use, the page you're on right now. :blush:""")
        st.write("""\n""")
        st.write("""Note: To use the application, you must be sure of some formats and follow some steps.""")
        st.markdown(
            """
            <h3> How to use this application: </h3>
            <ol>
                 <li> Export the Whatsapp group Chat.</li>
                 <li> Check date format for exported text file.</li>
                 <ul>
                     <li> If the format is [DD.MM.YY, HH:MM], select the first button.</li>
                     <li> If the format is [DD/MM/YY, HH:MM], select the second button.</li>
                     <li> If the format is [DD.MM.YY, HH:MM:SS], select the third button.</li>
                     <li> If the format doesn't match any of the above, this app can't work for you</li>
                 </ul>
                 <li> Upload the text file and select the time format</li>
            </ol>
            """,
            unsafe_allow_html=True
        )
        st.write("""\n""")
        st.markdown("<h4 style='text-align:center;'>Here We Go!</h4>", unsafe_allow_html=True)



    elif page == "Model Application / Örnek Uygulama":

        df = functions.txtToDf("Phoenix_Data.txt", "Format1")
        n_users, n_messages, n_days, avg_message_per_day, avg_message_per_user, max_len_message, min_len_message, \
            avg_len_message, user_max_len_message, n_words, max_word_message, min_word_message, avg_words, max_emoji = functions.df_general_stats(df)

        st.markdown("<h1 style='text-align:center;'>WhatsApp Group Chat Analysis</h1>",unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>Sample Model Application</h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:left;'>All Group Statistic</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:left;'>General Statistics of the Group</h3>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
        col1.metric("Number of Days:", n_days)
        col2.metric('Number of Users:', n_users)
        col3.metric("Number of Messages:", n_messages)
        col4.metric("Number of Words:", n_words)

        col5, col6, col7, col8 = st.columns([5, 5, 5, 5])
        col5.metric('Avg. Messages per User:', "{:.2f}".format(avg_message_per_user))
        col6.metric("Avg. Messages per Day:", "{:.2f}".format(avg_message_per_day))
        col7.metric('Avg. Len. of Msgs. (word):', "{:.2f}".format(avg_words))
        col8.metric("Avg Len. Of Msgs. (char):", "{:.2f}".format(avg_len_message))

        col9, col10, col11, col12 = st.columns([5, 5, 5, 5])
        col9.metric("Min. Len. Of Msgs (word): ", min_word_message)
        col10.metric("Max. Len. of Msgs (word):", max_word_message)
        col11.metric("Min. Len. of Msgs (char):", min_len_message)
        col12.metric("Max. Len. of Msgs (char):", max_len_message)

        col13, col14, col15, col16 = st.columns([10, 1, 1, 1])
        col13.metric('User Who Wrote the Longest:', user_max_len_message)

        st.write("""*The Longest Message*""")
        st.write(df[df["len_message"] == max_len_message]["message"].item())

        st.markdown("<h3 style='text-align:left;'>Conversation History Plot</h3>", unsafe_allow_html=True)
        # Create a line plot about number of messages based days
        x = df['date'].value_counts().sort_index()
        st.line_chart(x, use_container_width=True)

        col1, col2, col3 = st.columns([5, 5, 5])
        with col1:
            st.markdown("<h4 style='text-align:left;'>Top N Days</h4>", unsafe_allow_html=True)
            n = st.number_input('Enter the number of days you want to see', min_value=1, max_value=50, value=5, step=1)
            st.dataframe(functions.top_n_days(df, n), width = None)

        with col2:
            st.markdown("<h4 style='text-align:left;'>Top Emojis</h4>", unsafe_allow_html=True)
            n = st.number_input('Enter the number of emoji you want to see', min_value=1, max_value=50, value=5, step=1)
            st.dataframe(functions.most_emojis(df,n), width=None)

        with col3:
            st.markdown("<h4 style='text-align:left;'>Top N Users</h4>", unsafe_allow_html=True)
            n = st.number_input('Enter the number of users you want to see', min_value=1, max_value=50, value=5, step=1)
            st.dataframe(functions.top_n_user(df, n), width = None)

        st.markdown("<h3 style='text-align:left;'>Most Active Hours</h3>", unsafe_allow_html=True)
        grouped_by_time = df.groupby('hour').sum().sort_values(by='hour')
        grouped_by_time = grouped_by_time["message_count"]
        st.bar_chart(grouped_by_time, use_container_width=True)

        st.markdown("<h3 style='text-align:left;'>Most Active Days</h3>", unsafe_allow_html=True)
        grouped_by_dayt = df.groupby('day_t').sum().sort_values(by='day_t')
        grouped_by_dayt = grouped_by_dayt["message_count"]
        st.bar_chart(grouped_by_dayt, use_container_width=True)

        st.markdown("<h3 style='text_align:left;'> User Most Emoji</h3>", unsafe_allow_html=True)
        user_emoji_most = df.groupby("user").agg({'emoji_count':'sum'}).sort_values(by='emoji_count', ascending=False).head(10)
        st.bar_chart(user_emoji_most, use_container_width=True)

        st.markdown("<h3 style='text-align:left;'>Heatmap of Day-Hour</h3>", unsafe_allow_html=True)
        fig = px.imshow(pd.crosstab(df['day_t'], df['hour']))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<h3 style='text-align:left;'>Word-Cloud of Group</h3>", unsafe_allow_html=True)
        st.write("""Note: Turkish stopwords were removed in this process.""")
        # Display the generated image:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        wordcloud = functions.word_cloud_all(df)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

        ##########SELECTED USER STATISTICS##########

        st.markdown("<h2 style='text-align:left;'>Selected User Statistic</h2>", unsafe_allow_html=True)
        user_list = sorted(df["user"].unique().tolist())
        selected_user = st.selectbox('Select Username', user_list)

        st.markdown("<h3 style='text-align:left;'>General Statistics of the Selected User</h3>", unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns([5, 5, 5, 5, 5])
        col1.metric("Number of Days:", n_days)
        col2.metric('Number of Messages:', df[df["user"] == selected_user].shape[0])
        col3.metric("Avg. Msgs. per Day:", "{:.2f}".format(df[df["user"] == selected_user].shape[0] / n_days))
        col4.metric("Number of Words:", df[df["user"] == selected_user]["n_words"].sum())
        col5.metric("Avg. Words per Msgs.:", "{:.2f}".format(df[df["user"] == selected_user]["n_words"].sum() / df[df["user"] == selected_user].shape[0]))

        col6, col7, col8 = st.columns([5, 5, 5])
        col6.metric("Min. Len. of Msgs (char):", df[df["user"] == selected_user]["len_message"].min())
        col7.metric("Max. Len. of Msgs (char):", df[df["user"] == selected_user]["len_message"].max())
        col8.metric("Avg. Len. of Msgs (char):", "{:.2f}".format(df[df["user"] == selected_user]["len_message"].mean()))

        col9, col10, col11 = st.columns([5, 5, 5])
        col9.metric("Min. Len. of Msgs (word):", df[df["user"] == selected_user]["n_words"].min())
        col10.metric("Max. Len. of Msgs (word):", df[df["user"] == selected_user]["n_words"].max())
        col11.metric("Avg. Len. of Msgs (word):", "{:.2f}".format(df[df["user"] == selected_user]["n_words"].mean()))

        st.write("""*The Longest Message*""")
        st.write(df[(df["user"] == selected_user) & (df["len_message"] == df[df["user"] == selected_user]["len_message"].max())]["message"].item())

        st.markdown("<h3 style='text-align:left;'>Conversation History Plot</h3>", unsafe_allow_html=True)
        # Create a line plot about number of messages based days
        x = df[df["user"] == selected_user]['date'].value_counts().sort_index()
        st.line_chart(x, use_container_width=True)

        col1, col2, col3 = st.columns([5, 5, 5])
        with col1:
            st.markdown("<h3 style='text-align:left;'>Top N Days</h3>", unsafe_allow_html=True)
            n1 = st.number_input('Enter the number of days you want to see for user', min_value=1, max_value=50, value=5, step=1)
            user_df1 = df[df["user"] == selected_user]
            user_df1 = functions.top_n_days(user_df1, n1)
            st.dataframe(user_df1, width=None)

        with col2:
            st.markdown("<h4 style='text-align:left;'>Top Emojis</h4>", unsafe_allow_html=True)
            n1 = st.number_input('Enter the number of emoji you want to see for user', min_value=1, max_value=50, value=5, step=1)
            user_df2 = df[df["user"] == selected_user]
            user_df2 = functions.most_emojis(user_df2, n1)
            st.dataframe(user_df2, width=None)


        with col3:
            st.markdown("<h3 style='text-align:left;'>Top N Days Graph</h3>", unsafe_allow_html=True)
            st.bar_chart(user_df1["message_count"], use_container_width=True)

        st.markdown("<h3 style='text-align:left;'>Most Active Hours</h3>", unsafe_allow_html=True)
        grouped_by_time = df[df["user"] == selected_user]
        grouped_by_time = grouped_by_time.groupby('hour').sum().sort_values(by='hour')
        grouped_by_time = grouped_by_time["message_count"]
        st.bar_chart(grouped_by_time, use_container_width=True)

        st.markdown("<h3 style='text-align:left;'>Most Active Days</h3>", unsafe_allow_html=True)
        grouped_by_dayt = df[df["user"] == selected_user]
        grouped_by_dayt = df.groupby('day_t').sum().sort_values(by='day_t')
        grouped_by_dayt = grouped_by_dayt["message_count"]
        st.bar_chart(grouped_by_dayt, use_container_width=True)

        st.markdown("<h3 style='text-align:left;'>Heatmap of Day-Hour</h3>", unsafe_allow_html=True)
        heatmap_df = df[df["user"] == selected_user]
        fig = px.imshow(pd.crosstab(heatmap_df['day_t'], heatmap_df['hour']))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<h3 style='text-align:left;'>Word-Cloud of the User</h3>", unsafe_allow_html=True)
        st.write("""Note: Turkish stopwords were removed in this process.""")
        # Display the generated image:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        wordcloud_df = df[df["user"] == selected_user]
        wordcloud = functions.word_cloud_all(wordcloud_df)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    elif page == "Do Your Own Analysis / Kendi Analizinizi Yapın":

        st.markdown("<h1 style='text-align:center;'>WhatsApp Group Chat Analysis</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>Do Your Own Analysis</h2>", unsafe_allow_html=True)

        uploaded_file = st.sidebar.file_uploader("Upload a group chat txt file:", accept_multiple_files=False)
        selected_format = st.sidebar.selectbox('What is the date format?', ('DD.MM.YYYY HH:MM', 'DD/MM/YYYY, HH:MM', '[DD.MM.YYYY HH:MM:SS]'))

        if selected_format == 'DD.MM.YYYY HH:MM':
            time_format = "Format1"
        elif selected_format == 'DD/MM/YYYY, HH:MM':
            time_format = "Format2"
        elif selected_format == "[DD.MM.YYYY HH:MM:SS]":
            time_format = "Format3"

        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            data = bytes_data.decode(encoding='utf-8')

            df = functions.txtToDf_inputpage(data, time_format)
            n_users, n_messages, n_days, avg_message_per_day, avg_message_per_user, max_len_message, min_len_message, \
                avg_len_message, user_max_len_message, n_words, max_word_message, min_word_message, avg_words, max_emoji = functions.df_general_stats(df)

            st.markdown("<h2 style='text-align:left;'>All Group Statistic</h2>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:left;'>General Statistics of the Group</h3>", unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
            col1.metric("Number of Days:", n_days)
            col2.metric('Number of Users:', n_users)
            col3.metric("Number of Messages:", n_messages)
            col4.metric("Number of Words:", n_words)

            col5, col6, col7, col8 = st.columns([5, 5, 5, 5])
            col5.metric('Avg. Messages per User:', "{:.2f}".format(avg_message_per_user))
            col6.metric("Avg. Messages per Day:", "{:.2f}".format(avg_message_per_day))
            col7.metric('Avg. Len. of Msgs. (word):', "{:.2f}".format(avg_words))
            col8.metric("Avg Len. Of Msgs. (char):", "{:.2f}".format(avg_len_message))

            col9, col10, col11, col12 = st.columns([5, 5, 5, 5])
            col9.metric("Min. Len. Of Msgs (word): ", min_word_message)
            col10.metric("Max. Len. of Msgs (word):", max_word_message)
            col11.metric("Min. Len. of Msgs (char):", min_len_message)
            col12.metric("Max. Len. of Msgs (char):", max_len_message)

            col13, col14, col15, col16 = st.columns([10, 1, 1, 1])
            col13.metric('User Who Wrote the Longest:', user_max_len_message)

            st.write("""*The Longest Message*""")
            st.write(df[df["len_message"] == max_len_message]["message"].item())

            st.markdown("<h3 style='text-align:left;'>Conversation History Plot</h3>", unsafe_allow_html=True)
            # Create a line plot about number of messages based days
            x = df['date'].value_counts().sort_index()
            st.line_chart(x, use_container_width=True)

            col1, col2, col3 = st.columns([5, 5, 5])
            with col1:
                st.markdown("<h4 style='text-align:left;'>Top N Days</h4>", unsafe_allow_html=True)
                n = st.number_input('Enter the number of days you want to see', min_value=1, max_value=50, value=5, step=1)
                st.dataframe(functions.top_n_days(df, n), width = None)

            with col2:
                st.markdown("<h4 style='text-align:left;'>Top Emojis</h4>", unsafe_allow_html=True)
                n = st.number_input('Enter the number of users emoji you want to see', min_value=1, max_value=50, value=5,
                                    step=1)
                st.dataframe(functions.most_emojis(df, n), width=None)

            with col3:
                st.markdown("<h4 style='text-align:left;'>Top N Users</h4>", unsafe_allow_html=True)
                n = st.number_input('Enter the number of users you want to see', min_value=1, max_value=50, value=5, step=1)
                st.dataframe(functions.top_n_user(df, n), width = None)

            st.markdown("<h3 style='text-align:left;'>Most Active Hours</h3>", unsafe_allow_html=True)
            grouped_by_time = df.groupby('hour').sum().sort_values(by='hour')
            grouped_by_time = grouped_by_time["message_count"]
            st.bar_chart(grouped_by_time, use_container_width=True)

            st.markdown("<h3 style='text-align:left;'>Most Active Days</h3>", unsafe_allow_html=True)
            grouped_by_dayt = df.groupby('day_t').sum().sort_values(by='day_t')
            grouped_by_dayt = grouped_by_dayt["message_count"]
            st.bar_chart(grouped_by_dayt, use_container_width=True)

            st.markdown("<h3 style='text-align:left;'>Heatmap of Day-Hour</h3>", unsafe_allow_html=True)
            fig = px.imshow(pd.crosstab(df['day_t'], df['hour']))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<h3 style='text-align:left;'>Word-Cloud of Group</h3>", unsafe_allow_html=True)
            st.write("""Note: Turkish stopwords were removed in this process.""")
            # Display the generated image:
            st.set_option('deprecation.showPyplotGlobalUse', False)
            wordcloud = functions.word_cloud_all(df)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot()

            ##########SELECTED USER STATISTICS##########

            st.markdown("<h2 style='text-align:left;'>Selected User Statistic</h2>", unsafe_allow_html=True)
            user_list = sorted(df["user"].unique().tolist())
            selected_user = st.selectbox('Select Username', user_list)

            st.markdown("<h3 style='text-align:left;'>General Statistics of the Selected User</h3>", unsafe_allow_html=True)

            col1, col2, col3, col4, col5 = st.columns([5, 5, 5, 5, 5])
            col1.metric("Number of Days:", n_days)
            col2.metric('Number of Messages:', df[df["user"] == selected_user].shape[0])
            col3.metric("Avg. Msgs. per Day:", "{:.2f}".format(df[df["user"] == selected_user].shape[0] / n_days))
            col4.metric("Number of Words:", df[df["user"] == selected_user]["n_words"].sum())
            col5.metric("Avg. Words per Msgs.:", "{:.2f}".format(df[df["user"] == selected_user]["n_words"].sum() / df[df["user"] == selected_user].shape[0]))

            col6, col7, col8 = st.columns([5, 5, 5])
            col6.metric("Min. Len. of Msgs (char):", df[df["user"] == selected_user]["len_message"].min())
            col7.metric("Max. Len. of Msgs (char):", df[df["user"] == selected_user]["len_message"].max())
            col8.metric("Avg. Len. of Msgs (char):", "{:.2f}".format(df[df["user"] == selected_user]["len_message"].mean()))

            col9, col10, col11 = st.columns([5, 5, 5])
            col9.metric("Min. Len. of Msgs (word):", df[df["user"] == selected_user]["n_words"].min())
            col10.metric("Max. Len. of Msgs (word):", df[df["user"] == selected_user]["n_words"].max())
            col11.metric("Avg. Len. of Msgs (word):", "{:.2f}".format(df[df["user"] == selected_user]["n_words"].mean()))

            st.write("""*The Longest Message*""")
            st.write(df[(df["user"] == selected_user) & (df["len_message"] == df[df["user"] == selected_user]["len_message"].max())]["message"].item())

            st.markdown("<h3 style='text-align:left;'>Conversation History Plot</h3>", unsafe_allow_html=True)
            # Create a line plot about number of messages based days
            x = df[df["user"] == selected_user]['date'].value_counts().sort_index()
            st.line_chart(x, use_container_width=True)

            col1, col2, col3 = st.columns([5, 5, 5])
            with col1:
                st.markdown("<h4 style='text-align:left;'>Top N Days</h4>", unsafe_allow_html=True)
                n1 = st.number_input('Enter the number of days you want to see for user', min_value=1, max_value=50, value=5, step=1)
                user_df1 = df[df["user"] == selected_user]
                user_df1 = functions.top_n_days(user_df1, n1)
                st.dataframe(user_df1, width=None)

            with col2:
                st.markdown("<h4 style='text-align:left;'>Top Emojis</h4>", unsafe_allow_html=True)
                n2 = st.number_input('Enter the number of emoji you want to see', min_value=1, max_value=50, value=5, step=1)
                user_df2 = df[df["user"] == selected_user]
                user_df2 = functions.most_emojis(user_df2, n2)
                st.dataframe(user_df2, width=None)

            with col3:
                st.markdown("<h4 style='text-align:left;'>Top N Days Graph</h4>", unsafe_allow_html=True)
                st.bar_chart(user_df1["message_count"], use_container_width=True)

            st.markdown("<h3 style='text-align:left;'>Most Active Hours</h3>", unsafe_allow_html=True)
            grouped_by_time = df[df["user"] == selected_user]
            grouped_by_time = grouped_by_time.groupby('hour').sum().sort_values(by='hour')
            grouped_by_time = grouped_by_time["message_count"]
            st.bar_chart(grouped_by_time, use_container_width=True)

            st.markdown("<h3 style='text-align:left;'>Most Active Days</h3>", unsafe_allow_html=True)
            grouped_by_dayt = df[df["user"] == selected_user]
            grouped_by_dayt = df.groupby('day_t').sum().sort_values(by='day_t')
            grouped_by_dayt = grouped_by_dayt["message_count"]
            st.bar_chart(grouped_by_dayt, use_container_width=True)

            st.markdown("<h3 style='text-align:left;'>Heatmap of Day-Hour</h3>", unsafe_allow_html=True)
            heatmap_df = df[df["user"] == selected_user]
            fig = px.imshow(pd.crosstab(heatmap_df['day_t'], heatmap_df['hour']))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<h3 style='text-align:left;'>Word-Cloud of Group</h3>", unsafe_allow_html=True)
            st.write("""Note: Turkish stopwords were removed in this process.""")
            # Display the generated image:
            st.set_option('deprecation.showPyplotGlobalUse', False)
            wordcloud_df = df[df["user"] == selected_user]
            wordcloud = functions.word_cloud_all(wordcloud_df)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot()

elif selected_language == "Türkçe":

    if page == "How to Use / Nasıl Kullanılır":
        st.markdown("<h1 style='text-align:center;'>WhatsApp Sohbet Analiz</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>Nasıl Kullanılır</h2>", unsafe_allow_html=True)
        st.write(
            """Bu proje WhatsApp sohbetlerini analiz eden, temel istatistiksel bilgileri görselleştiren ve kullanıcıya sunan bir uygulamadır.""")
        st.write(
            """Örnek Uygulama bölümünde örnek projeyi inceleyebilir ve Kendi Analizinizi Yapın bölümünde kendi analizinizi yapabilirsiniz.""")
        st.write("""Ama önce, şu anda bulunduğunuz sayfa olan Nasıl Kullanılır'ı iyice okumayı unutmayın. :blush:""")
        st.write("""\n""")
        st.write("""Not: Uygulamayı kullanmak için bazı formatlardan emin olmanız ve bazı adımları takip etmeniz gerekmektedir.""")
        st.markdown(
            """
            <h3> Uygulama Nasil Kullanilir: </h3>
            <ol>
                 <li> Group konusma dosyanizi export edin.</li>
                 <li> Export etmis oldugunuz dosyanin tarih formatini kontrol edin.</li>
                 <ul>
                     <li> Eger ki format [DD.MM.YY, HH:MM], ilk butonu secin.</li>
                     <li> Eger ki format [DD/MM/YY, HH:MM], ikinci butonu secin.</li>
                     <li> Eger ki format  [DD.MM.YY, HH:MM:SS], ucuncu butonu secin.</li>
                     <li> Eger ki dosya formatiniz yukaridaki hic birisi ile uyusmuyorsa, bu uygulama size gore degil. </li>
                 </ul>
                 <li> Upload the text file ad select the time format</li>
            </ol>
            """,
            unsafe_allow_html=True
        )
        st.write("""\n""")
        st.markdown("<h4 style='text-align:center;'>Hadi Başlayalım!</h4>", unsafe_allow_html=True)



    elif page == "Model Application / Örnek Uygulama":

        df = functions.txtToDf("Phoenix_Data.txt", "Format1")
        n_users, n_messages, n_days, avg_message_per_day, avg_message_per_user, max_len_message, min_len_message,\
            avg_len_message, user_max_len_message, n_words, max_word_message, min_word_message, avg_words, max_emoji = functions.df_general_stats(
            df)

        st.markdown("<h1 style='text-align:center;'>WhatsApp Sohbet Analizi</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>Örnek Proje Uygulaması</h2>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:left;'>Toplu Grup Analizi</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:left;'>Grubun Genel İstatistikleri</h3>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
        col1.metric("Gün Sayısı:", n_days)
        col2.metric('Kullanıcı Sayısı:', n_users)
        col3.metric("Mesaj Sayısı:", n_messages)
        col4.metric("Kelime Sayısı:", n_words)

        col5, col6, col7, col8 = st.columns([5, 5, 5, 5])
        col5.metric('Kullanıcı Başına Ort. Mesaj:', "{:.2f}".format(avg_message_per_user))
        col6.metric("Gün Başına Ort. Mesaj:", "{:.2f}".format(avg_message_per_day))
        col7.metric('Ort. Mesaj Uzun. (kelime):', "{:.2f}".format(avg_words))
        col8.metric("Ort. Mesaj Uzun. (karakter):", "{:.2f}".format(avg_len_message))

        col9, col10, col11, col12 = st.columns([5, 5, 5, 5])
        col9.metric("En Kısa Msj. Uzun. (kelime): ", min_word_message)
        col10.metric("En Uzun Msj. Uzun. (kelime):", max_word_message)
        col11.metric("En Kısa Msj. Uzun. (karakter):", min_len_message)
        col12.metric("En Uzun Msj. Uzun. (karakter):", max_len_message)

        col13, col14, col15, col16 = st.columns([10, 1, 1, 1])
        col13.metric('En Uzun Mesajı Yazan:', user_max_len_message)

        st.write("""*En Uzun Mesaj*""")
        st.write(df[df["len_message"] == max_len_message]["message"].item())

        st.markdown("<h3 style='text-align:left;'>Konuşma Geçmişi Grafiği</h3>", unsafe_allow_html=True)
        # Create a line plot about number of messages based days
        x = df['date'].value_counts().sort_index()
        st.line_chart(x, use_container_width=True)

        col1, col2, col3 = st.columns([6, 5, 5])
        with col1:
            st.markdown("<h4 style='text-align:left;'>En Aktif Günler</h4>", unsafe_allow_html=True)
            n = st.number_input('Kaç gün görmek istediğinizi seçiniz', min_value=1, max_value=50, value=5, step=1)
            st.dataframe(functions.top_n_days(df, n), width=None)

        with col2:
            st.markdown("<h4 style='text-align:left;'>En Cok Kullanilan Emojiler</h4>", unsafe_allow_html=True)
            n = st.number_input('Kac tane emoji gormek istediginizi seciniz', min_value=1, max_value=50, value=5, step=1)
            st.dataframe(functions.most_emojis(df, n), width=None)

        with col3:
            st.markdown("<h4 style='text-align:left;'>En Aktif Kullanıcılar</h4>", unsafe_allow_html=True)
            n = st.number_input('Kaç kullanıcı görmek istediğinizi seçiniz', min_value=1, max_value=50, value=5, step=1)
            st.dataframe(functions.top_n_user(df, n), width=None)

        st.markdown("<h3 style='text-align:left;'>En Aktif Saatler</h3>", unsafe_allow_html=True)
        grouped_by_time = df.groupby('hour').sum().sort_values(by='hour')
        grouped_by_time = grouped_by_time["message_count"]
        st.bar_chart(grouped_by_time, use_container_width=True)

        st.markdown("<h3 style='text-align:left;'>En Aktif Günler</h3>", unsafe_allow_html=True)
        grouped_by_dayt = df.groupby('day_t').sum().sort_values(by='day_t')
        grouped_by_dayt = grouped_by_dayt["message_count"]
        st.bar_chart(grouped_by_dayt, use_container_width=True)
        st.write("""Mon: Pazartesi & Tue: Salı & Wed: Çarşamba & Thu: Perşembe & Fri: Cuma & Sat: Cumartesi & Sun: Pazar""")

        st.markdown("<h3 style='text_align:left;'> En cok Emoji Kullananlar</h3>", unsafe_allow_html=True)
        user_emoji_most = df.groupby("user").agg({'emoji_count':'sum'}).sort_values(by='emoji_count', ascending=False).head(10)
        st.bar_chart(user_emoji_most, use_container_width=True)


        st.markdown("<h3 style='text-align:left;'>Gün-Saat Isı Haritası</h3>", unsafe_allow_html=True)
        fig = px.imshow(pd.crosstab(df['day_t'], df['hour']))
        st.plotly_chart(fig, use_container_width=True)
        st.write("""Mon: Pazartesi & Tue: Salı & Wed: Çarşamba & Thu: Perşembe & Fri: Cuma & Sat: Cumartesi & Sun: Pazar""")

        st.markdown("<h3 style='text-align:left;'>Grubun Kelime Bulutu</h3>", unsafe_allow_html=True)
        st.write("""Not: Türkçe stopwords (Bu, şu vb.) kelimeler çıkartılmıştır.""")
        # Display the generated image:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        wordcloud = functions.word_cloud_all(df)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

        ##########SELECTED USER STATISTICS##########

        st.markdown("<h2 style='text-align:left;'>Seçilen Kullanıcı İstatistikler</h2>", unsafe_allow_html=True)
        user_list = sorted(df["user"].unique().tolist())
        selected_user = st.selectbox('Kullanıcı Seçiniz', user_list)

        st.markdown("<h3 style='text-align:left;'>Kullanıcının Genel İstatistikleri</h3>", unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns([5, 5, 5, 5, 5])
        col1.metric("Gün Sayısı:", n_days)
        col2.metric('Mesaj Sayısı:', df[df["user"] == selected_user].shape[0])
        col3.metric("Gün Başına Ort. Mesaj:", "{:.2f}".format(df[df["user"] == selected_user].shape[0] / n_days))
        col4.metric("Kelime Sayısı:", df[df["user"] == selected_user]["n_words"].sum())
        col5.metric("Msj. Başına Ort. Kelime:", "{:.2f}".format(
            df[df["user"] == selected_user]["n_words"].sum() / df[df["user"] == selected_user].shape[0]))

        col6, col7, col8 = st.columns([5, 5, 5])
        col6.metric("En Kısa Msj. Uzun. (karakter):", df[df["user"] == selected_user]["len_message"].min())
        col7.metric("En Uzun Msj. Uzun. (karakter):", df[df["user"] == selected_user]["len_message"].max())
        col8.metric("Ort. Mesaj Uzunluğu (karakter)", "{:.2f}".format(df[df["user"] == selected_user]["len_message"].mean()))

        col9, col10, col11 = st.columns([5, 5, 5])
        col9.metric("En Kısa Msj. Uzun. (kelime):", df[df["user"] == selected_user]["n_words"].min())
        col10.metric("En Uzun Msj. Uzun. (kelime):", df[df["user"] == selected_user]["n_words"].max())
        col11.metric("Ort. Mesaj Uzunluğu (kelime):", "{:.2f}".format(df[df["user"] == selected_user]["n_words"].mean()))

        st.write("""*En Uzun Mesaj*""")
        st.write(df[(df["user"] == selected_user) & (
                    df["len_message"] == df[df["user"] == selected_user]["len_message"].max())]["message"].item())

        st.markdown("<h3 style='text-align:left;'>Konuşma Geçmişi Grafiği</h3>", unsafe_allow_html=True)
        # Create a line plot about number of messages based days
        x = df[df["user"] == selected_user]['date'].value_counts().sort_index()
        st.line_chart(x, use_container_width=True)

        col1, col2, col3 = st.columns([6, 5, 5])
        with col1:
            st.markdown("<h4 style='text-align:left;'>En Aktif Günler</h4>", unsafe_allow_html=True)
            n1 = st.number_input('Kullanıcı için görmek istediğiniz gün sayısını giriniz', min_value=1, max_value=50,value=5, step=1)
            st.write("""date: gün & message_count: mesaj sayısı""")
            user_df1 = df[df["user"] == selected_user]
            user_df1 = functions.top_n_days(user_df1, n1)
            st.dataframe(user_df1, width=None)

        with col2:
            st.markdown("<h4 style='text-align:left;'>En Cok Kullanilan Emojiler</h4>", unsafe_allow_html=True)
            n1 = st.number_input('Kullanici icin kac tane emoji gormek istediginizi seciniz', min_value=1, max_value=50, value=5, step=1)
            user_df2 = df[df["user"] == selected_user]
            user_df2 = functions.most_emojis(user_df2, n1)
            st.dataframe(user_df2, width=None)

        with col3:
            st.markdown("<h4 style='text-align:left;'>En Aktif Günler Grafiği</h4>", unsafe_allow_html=True)
            st.bar_chart(user_df1["message_count"], use_container_width=True)

        st.markdown("<h3 style='text-align:left;'>En Aktif Saatler</h3>", unsafe_allow_html=True)
        grouped_by_time = df[df["user"] == selected_user]
        grouped_by_time = grouped_by_time.groupby('hour').sum().sort_values(by='hour')
        grouped_by_time = grouped_by_time["message_count"]
        st.bar_chart(grouped_by_time, use_container_width=True)

        st.markdown("<h3 style='text-align:left;'>En Aktif Günler</h3>", unsafe_allow_html=True)
        grouped_by_dayt = df[df["user"] == selected_user]
        grouped_by_dayt = df.groupby('day_t').sum().sort_values(by='day_t')
        grouped_by_dayt = grouped_by_dayt["message_count"]
        st.bar_chart(grouped_by_dayt, use_container_width=True)
        st.write("""Mon: Pazartesi & Tue: Salı & Wed: Çarşamba & Thu: Perşembe & Fri: Cuma & Sat: Cumartesi & Sun: Pazar""")

        st.markdown("<h3 style='text-align:left;'>Gün-Saat Isı Haritası</h3>", unsafe_allow_html=True)
        heatmap_df = df[df["user"] == selected_user]
        fig = px.imshow(pd.crosstab(heatmap_df['day_t'], heatmap_df['hour']))
        st.plotly_chart(fig, use_container_width=True)
        st.write("""Mon: Pazartesi & Tue: Salı & Wed: Çarşamba & Thu: Perşembe & Fri: Cuma & Sat: Cumartesi & Sun: Pazar""")

        st.markdown("<h3 style='text-align:left;'>Kullanıcının Kelime Bulutu</h3>", unsafe_allow_html=True)
        st.write("""Not: Türkçe stopwords (Bu, şu vb.) kelimeler çıkartılmıştır.""")
        # Display the generated image:
        st.set_option('deprecation.showPyplotGlobalUse', False)
        wordcloud_df = df[df["user"] == selected_user]
        wordcloud = functions.word_cloud_all(wordcloud_df)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()

    elif page == "Do Your Own Analysis / Kendi Analizinizi Yapın":

        st.markdown("<h1 style='text-align:center;'>WhatsApp Sohbet Analizi</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>Kendi Analizinizi Yapın</h2>", unsafe_allow_html=True)

        uploaded_file = st.sidebar.file_uploader("Sohbet metin dosyası yükleyin:", accept_multiple_files=False)
        selected_format = st.sidebar.selectbox('Tarih formatını seçiniz:',
                                               ('GG.AA.YYYY SS:DD', 'GG/AA/YYYY, SS:DD', '[GG.AA.YYYY SS:DD:SS]'))

        if selected_format == 'GG.AA.YYYY SS:DD':
            time_format = "Format1"
        elif selected_format == 'GG/AA/YYYY, SS:DD':
            time_format = "Format2"
        elif selected_format == "[GG.AA.YYYY SS:DD:SS]":
            time_format = "Format3"

        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            data = bytes_data.decode(encoding='utf-8')

            df = functions.txtToDf_inputpage(data, time_format)
            n_users, n_messages, n_days, avg_message_per_day, avg_message_per_user, max_len_message, min_len_message, \
                avg_len_message, user_max_len_message, n_words, max_word_message, min_word_message, avg_words, max_emoji = functions.df_general_stats(
                df)

            st.markdown("<h2 style='text-align:left;'>Toplu Grup Analizi</h2>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:left;'>Grubun Genel İstatistikleri</h3>", unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
            col1.metric("Gün Sayısı:", n_days)
            col2.metric('Kullanıcı Sayısı:', n_users)
            col3.metric("Mesaj Sayısı:", n_messages)
            col4.metric("Kelime Sayısı:", n_words)

            col5, col6, col7, col8 = st.columns([5, 5, 5, 5])
            col5.metric('Kullanıcı Başına Ort. Mesaj', "{:.2f}".format(avg_message_per_user))
            col6.metric("Gün Başına Ort. Mesaj:", "{:.2f}".format(avg_message_per_day))
            col7.metric('Ort. Mesaj Uzun. (kelime):', "{:.2f}".format(avg_words))
            col8.metric("Ort. Mesaj Uzun. (karakter):", "{:.2f}".format(avg_len_message))

            col9, col10, col11, col12 = st.columns([5, 5, 5, 5])
            col9.metric("En Kısa Msj. Uzun. (kelime): ", min_word_message)
            col10.metric("En Uzun Msj. Uzun. (kelime):", max_word_message)
            col11.metric("En Kısa Msj. Uzun. (karakter):", min_len_message)
            col12.metric("En Uzun Msj. Uzun. (karakter):", max_len_message)

            col13, col14, col15, col16 = st.columns([10, 1, 1, 1])
            col13.metric('En Uzun Mesajı Yazan:', user_max_len_message)

            st.write("""*En Uzun Mesaj*""")
            st.write(df[df["len_message"] == max_len_message]["message"].item())

            st.markdown("<h3 style='text-align:left;'>Konuşma Geçmişi Grafiği</h3>", unsafe_allow_html=True)
            # Create a line plot about number of messages based days
            x = df['date'].value_counts().sort_index()
            st.line_chart(x, use_container_width=True)

            col1, col2, col3 = st.columns([5, 5, 5])
            with col1:
                st.markdown("<h4 style='text-align:left;'>En Aktif Günler</h4>", unsafe_allow_html=True)
                n = st.number_input('Kaç gün görmek istediğinizi seçiniz', min_value=1, max_value=50, value=5,
                                    step=1)
                st.write("""date: gün & message_count: mesaj sayısı""")
                st.dataframe(functions.top_n_days(df, n), width=None)

            with col2:
                st.markdown("<h4 style='text-align:left;'>Cok Kullanilan Emojiler</h4>", unsafe_allow_html=True)
                n = st.number_input('Kac tane emoji gormek istediginizi seciniz', min_value=1, max_value=50, value=5,
                                    step=1)

                st.dataframe(functions.most_emojis(df, n), width=None)

            with col3:
                st.markdown("<h4 style='text-align:left;'>En Aktif Kullanıcılar</h4>", unsafe_allow_html=True)
                n = st.number_input('Kaç kullanıcı görmek istediğinizi seçiniz', min_value=1, max_value=50, value=5,
                                    step=1)
                st.write("""user: kullanıcı & message_count: mesaj sayısı""")
                st.dataframe(functions.top_n_user(df, n), width=None)

            st.markdown("<h3 style='text-align:left;'>En Aktif Saatler</h3>", unsafe_allow_html=True)
            grouped_by_time = df.groupby('hour').sum().sort_values(by='hour')
            grouped_by_time = grouped_by_time["message_count"]
            st.bar_chart(grouped_by_time, use_container_width=True)

            st.markdown("<h3 style='text-align:left;'>En Aktif Günler</h3>", unsafe_allow_html=True)
            grouped_by_dayt = df.groupby('day_t').sum().sort_values(by='day_t')
            grouped_by_dayt = grouped_by_dayt["message_count"]
            st.bar_chart(grouped_by_dayt, use_container_width=True)
            st.write("""Mon: Pazartesi & Tue: Salı & Wed: Çarşamba & Thu: Perşembe & Fri: Cuma & Sat: Cumartesi & Sun: Pazar""")

            st.markdown("<h3 style='text-align:left;'>Gün-Saat Isı Haritası</h3>", unsafe_allow_html=True)
            fig = px.imshow(pd.crosstab(df['day_t'], df['hour']))
            st.plotly_chart(fig, use_container_width=True)
            st.write("""Mon: Pazartesi & Tue: Salı & Wed: Çarşamba & Thu: Perşembe & Fri: Cuma & Sat: Cumartesi & Sun: Pazar""")


            st.markdown("<h3 style='text-align:left;'>Grubun Kelime Bulutu</h3>", unsafe_allow_html=True)
            st.write("""Not: Türkçe stopwords (Bu, şu vb.) kelimeler çıkartılmıştır.""")
            # Display the generated image:
            st.set_option('deprecation.showPyplotGlobalUse', False)
            wordcloud = functions.word_cloud_all(df)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot()

            ##########SELECTED USER STATISTICS##########

            st.markdown("<h2 style='text-align:left;'>Seçilen Kullanıcı İstatistikleri</h2>", unsafe_allow_html=True)
            user_list = sorted(df["user"].unique().tolist())
            selected_user = st.selectbox('Kullanıcı Seçiniz', user_list)

            st.markdown("<h3 style='text-align:left;'>Kullanıcının Genel İstatistikleri</h3>", unsafe_allow_html=True)

            col1, col2, col3, col4, col5 = st.columns([5, 5, 5, 5, 5])
            col1.metric("Gün Sayısı:", n_days)
            col2.metric('Mesaj Sayısı:', df[df["user"] == selected_user].shape[0])
            col3.metric("Gün Başına Ort. Mesaj:", "{:.2f}".format(df[df["user"] == selected_user].shape[0] / n_days))
            col4.metric("Kelime Sayısı:", df[df["user"] == selected_user]["n_words"].sum())
            col5.metric("Msj. Başına Ort. Kelime:", "{:.2f}".format(
                df[df["user"] == selected_user]["n_words"].sum() / df[df["user"] == selected_user].shape[0]))

            col6, col7, col8 = st.columns([5, 5, 5])
            col6.metric("En Kısa Msj. Uzun. (karakter):", df[df["user"] == selected_user]["len_message"].min())
            col7.metric("En Uzun Msj. Uzun. (karakter):", df[df["user"] == selected_user]["len_message"].max())
            col8.metric("Ort. Mesaj Uzunluğu (karakter):",
                        "{:.2f}".format(df[df["user"] == selected_user]["len_message"].mean()))

            col9, col10, col11 = st.columns([5, 5, 5])
            col9.metric("En Kısa Msj. Uzun. (kelime):", df[df["user"] == selected_user]["n_words"].min())
            col10.metric("En Uzun Msj. Uzun. (kelime):", df[df["user"] == selected_user]["n_words"].max())
            col11.metric("Ort. Mesaj Uzunluğu (kelime):",
                         "{:.2f}".format(df[df["user"] == selected_user]["n_words"].mean()))

            st.write("""*En Uzun Mesaj*""")
            st.write(df[(df["user"] == selected_user) & (
                        df["len_message"] == df[df["user"] == selected_user]["len_message"].max())]["message"].item())

            st.markdown("<h3 style='text-align:left;'>Konuşma Geçmişi Grafiği</h3>", unsafe_allow_html=True)
            # Create a line plot about number of messages based days
            x = df[df["user"] == selected_user]['date'].value_counts().sort_index()
            st.line_chart(x, use_container_width=True)

            col1, col2, col3 = st.columns([5, 5, 5])
            with col1:
                st.markdown("<h4 style='text-align:left;'>En Aktif Günler</h4>", unsafe_allow_html=True)
                n1 = st.number_input('Kullanıcı için görmek istediğiniz gün sayısını giriniz', min_value=1, max_value=50,
                                     value=5, step=1)
                user_df1 = df[df["user"] == selected_user]
                user_df1 = functions.top_n_days(user_df1, n1)
                st.dataframe(user_df1, width=None)

            with col2:
                st.markdown("<h4 style='text-align:left;'>En Cok Kullanilan Emojiler</h4>", unsafe_allow_html=True)
                n2 = st.number_input('Bu Kullanici icin Kac tane emoji gormek istediginizi seciniz', min_value=1, max_value=50, value=5,step=1)
                user_df2 = df[df["user"] == selected_user]
                user_df2 = functions.most_emojis(user_df2, n2)
                st.dataframe(user_df2, width=None)

            with col3:
                st.markdown("<h4 style='text-align:left;'>En Aktif Günler Grafiği</h4f>", unsafe_allow_html=True)
                st.bar_chart(user_df1["message_count"], use_container_width=True)

            st.markdown("<h3 style='text-align:left;'>En Aktif Saatler</h3>", unsafe_allow_html=True)
            grouped_by_time = df[df["user"] == selected_user]
            grouped_by_time = grouped_by_time.groupby('hour').sum().sort_values(by='hour')
            grouped_by_time = grouped_by_time["message_count"]
            st.bar_chart(grouped_by_time, use_container_width=True)

            st.markdown("<h3 style='text-align:left;'>En Aktif Günler</h3>", unsafe_allow_html=True)
            grouped_by_dayt = df[df["user"] == selected_user]
            grouped_by_dayt = df.groupby('day_t').sum().sort_values(by='day_t')
            grouped_by_dayt = grouped_by_dayt["message_count"]
            st.bar_chart(grouped_by_dayt, use_container_width=True)
            st.write(
                """Mon: Pazartesi & Tue: Salı & Wed: Çarşamba & Thu: Perşembe & Fri: Cuma & Sat: Cumartesi & Sun: Pazar""")

            st.markdown("<h3 style='text-align:left;'>Gün-Saat Isı Haritası</h3>", unsafe_allow_html=True)
            heatmap_df = df[df["user"] == selected_user]
            fig = px.imshow(pd.crosstab(heatmap_df['day_t'], heatmap_df['hour']))
            st.plotly_chart(fig, use_container_width=True)
            st.write(
                """Mon: Pazartesi & Tue: Salı & Wed: Çarşamba & Thu: Perşembe & Fri: Cuma & Sat: Cumartesi & Sun: Pazar""")

            st.markdown("<h3 style='text-align:left;'>Kullanıcının Kelime Bulutu</h3>", unsafe_allow_html=True)
            st.write("""Not: Türkçe stopwords (Bu, şu vb.) kelimeler çıkartılmıştır.""")
            # Display the generated image:
            st.set_option('deprecation.showPyplotGlobalUse', False)
            wordcloud_df = df[df["user"] == selected_user]
            wordcloud = functions.word_cloud_all(wordcloud_df)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot()