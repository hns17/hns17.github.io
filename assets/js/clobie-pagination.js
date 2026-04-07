document.addEventListener('DOMContentLoaded', () => {
  const pagedLists = document.querySelectorAll('.clobie-list[data-page-size]');

  pagedLists.forEach((list, listIndex) => {
    const pageSize = parseInt(list.dataset.pageSize || '5', 10);
    const items = Array.from(list.children).filter((el) => el.matches('article, .clobie-card, .clobie-gallery__item, a, div'));
    if (items.length <= pageSize) return;

    let currentPage = 1;
    const totalPages = Math.ceil(items.length / pageSize);

    const nav = document.createElement('div');
    nav.className = 'clobie-pagination';
    nav.setAttribute('data-list-index', String(listIndex));

    const prevBtn = document.createElement('button');
    prevBtn.type = 'button';
    prevBtn.className = 'clobie-pagination__btn';
    prevBtn.textContent = '이전';

    const status = document.createElement('span');
    status.className = 'clobie-pagination__status';

    const nextBtn = document.createElement('button');
    nextBtn.type = 'button';
    nextBtn.className = 'clobie-pagination__btn';
    nextBtn.textContent = '다음';

    nav.append(prevBtn, status, nextBtn);
    list.after(nav);

    const render = () => {
      const start = (currentPage - 1) * pageSize;
      const end = start + pageSize;
      items.forEach((item, idx) => {
        item.style.display = idx >= start && idx < end ? '' : 'none';
      });
      prevBtn.disabled = currentPage === 1;
      nextBtn.disabled = currentPage === totalPages;
      status.textContent = `${currentPage} / ${totalPages}`;
    };

    prevBtn.addEventListener('click', () => {
      if (currentPage > 1) {
        currentPage -= 1;
        render();
        list.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });

    nextBtn.addEventListener('click', () => {
      if (currentPage < totalPages) {
        currentPage += 1;
        render();
        list.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });

    render();
  });
});
