document.addEventListener('DOMContentLoaded', () => {
  const formatRelativeTime = (isoString) => {
    const target = new Date(isoString).getTime();
    if (Number.isNaN(target)) return '';
    const diffMs = Date.now() - target;
    const seconds = Math.max(0, Math.floor(diffMs / 1000));
    if (seconds < 60) return `${seconds}초 전`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}분 전`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}시간 전`;
    const days = Math.floor(hours / 24);
    if (days < 7) return `${days}일 전`;
    const weeks = Math.floor(days / 7);
    if (weeks < 5) return `${weeks}주 전`;
    const months = Math.floor(days / 30);
    return `${months}개월 전`;
  };

  document.querySelectorAll('.clobie-card--timed[data-published-at]').forEach((card) => {
    const ageNode = card.querySelector('.clobie-age');
    if (!ageNode) return;
    ageNode.textContent = formatRelativeTime(card.dataset.publishedAt);
  });

  const pagedLists = document.querySelectorAll('.clobie-list[data-page-size]');

  pagedLists.forEach((list, listIndex) => {
    const pageSize = parseInt(list.dataset.pageSize || '5', 10);
    const items = Array.from(list.children).filter((el) => el.matches('article, .clobie-card, .clobie-gallery__item, a, div'));
    if (items.length <= pageSize) return;

    const pageParam = `page-${listIndex + 1}`;
    const readPageFromUrl = () => {
      const params = new URLSearchParams(window.location.search);
      const raw = parseInt(params.get(pageParam) || '1', 10);
      return Number.isFinite(raw) && raw > 0 ? raw : 1;
    };
    const writePageToUrl = (page) => {
      const url = new URL(window.location.href);
      if (page <= 1) {
        url.searchParams.delete(pageParam);
      } else {
        url.searchParams.set(pageParam, String(page));
      }
      window.history.replaceState({ ...(window.history.state || {}), [pageParam]: page }, '', url);
    };

    const totalPages = Math.ceil(items.length / pageSize);
    let currentPage = Math.min(readPageFromUrl(), totalPages);

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
      currentPage = Math.max(1, Math.min(currentPage, totalPages));
      const start = (currentPage - 1) * pageSize;
      const end = start + pageSize;
      items.forEach((item, idx) => {
        item.style.display = idx >= start && idx < end ? '' : 'none';
      });
      prevBtn.disabled = currentPage === 1;
      nextBtn.disabled = currentPage === totalPages;
      status.textContent = `${currentPage} / ${totalPages}`;
      writePageToUrl(currentPage);
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

    window.addEventListener('popstate', () => {
      currentPage = Math.min(readPageFromUrl(), totalPages);
      render();
    });

    render();
  });
});
